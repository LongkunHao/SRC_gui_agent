#!/usr/bin/env python3
"""Parallel rollout runner for Speculative Rollback Correction.

This is the data-collection counterpart to ``run_eval.py``.
For each task it runs the K-step branch / teacher review / rollback
loop, then calls the hard verifier and admits successful trajectories
into a QD archive.

Output directory is tagged ``{model}_{ts}_rollout`` (instead of
``..._parallel``) so logs are easy to distinguish from evaluation runs.

Usage:
    python src/run_rollout.py \\
        --workers 4 --K 3 --web-app apps/gmail \\
        --teacher-base-url http://localhost:9002/v1 \\
        --teacher-model Qwen3.6-27B
"""

from __future__ import annotations

import argparse
import asyncio
import json
import os
import shutil
import sys
from datetime import datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

# IMPORTANT: load .env BEFORE importing rollout_agent / vision_agents because
# Qwen35VLAgent reads QWEN_MODEL / QWEN_BASE_URL at class-definition time.
from dotenv import load_dotenv
load_dotenv()

from qd_archive import QDArchive
from report import generate_report
from rollout_agent import BranchingRolloutAgent, RolloutAgent
from run_eval import (
    BG_GREEN, BG_RED, BG_YELLOW, BOLD, CYAN, DIFF_COLOR, DIM, GREEN,
    MAGENTA, RED, RESET, WHITE, YELLOW,
)
from server import start_server, stop_server, wait_for_server
from tasks import TASK_TIMEOUT, filter_tasks, load_tasks, run_task
from teacher_review import TeacherReviewer


STUCK_MARKERS = (
    "Connection refused",
    "CDP",
    "Browser unrecoverable",
    "consecutive failures",
    "Agent crashed",
    "Task started but did not finish",
)

AGENT_SETUP_TIMEOUT = float(os.environ.get("ROLLOUT_AGENT_SETUP_TIMEOUT", "75"))
AGENT_RESTART_TIMEOUT = float(os.environ.get("ROLLOUT_AGENT_RESTART_TIMEOUT", "60"))
AGENT_TEARDOWN_TIMEOUT = float(os.environ.get("ROLLOUT_AGENT_TEARDOWN_TIMEOUT", "30"))


def _looks_stuck_result(result: dict) -> bool:
    """Return True for retryable/incomplete task result placeholders."""
    if result.get("passed"):
        return False
    if result.get("status") == "timeout":
        return False
    if result.get("status") == "incomplete" or result.get("retryable"):
        return True
    steps = result.get("steps", 0)
    text = " ".join([
        str(result.get("verifier_message", "")),
        " ".join(str(e) for e in (result.get("errors") or [])),
    ])
    return (steps in (-1, 0)) and any(m in text for m in STUCK_MARKERS)


def _failed_placeholder(task: dict, *, status: str, message: str) -> dict:
    return {
        "task_id": task["id"],
        "difficulty": task.get("difficulty", ""),
        "instruction": task["instruction"],
        "passed": False,
        "verifier_message": message,
        "elapsed": 0,
        "steps": -1,
        "is_done": False,
        "final_result": None,
        "errors": [message],
        "status": status,
        "retryable": status in {"incomplete", "error"},
    }


def _write_result(task_dir: Path, result: dict) -> None:
    task_dir.mkdir(parents=True, exist_ok=True)
    with open(task_dir / "result.json", "w") as f:
        json.dump(result, f, indent=2)


def _prepare_task_artifacts(task_dir: Path, qd_root: Path, task_id: str) -> None:
    """Start a task from a clean per-task directory and archive slot."""
    if task_dir.is_dir():
        shutil.rmtree(task_dir)
    task_qd_dir = qd_root / task_id
    if task_qd_dir.is_dir():
        shutil.rmtree(task_qd_dir)
    task_dir.mkdir(parents=True, exist_ok=True)


async def _run_lifecycle_step(
    coro,
    *,
    timeout: float,
    tag: str,
    label: str,
) -> bool:
    try:
        await asyncio.wait_for(coro, timeout=timeout)
        return True
    except asyncio.TimeoutError:
        print(f"  {tag} {RED}{label} timed out after {timeout:g}s{RESET}")
    except Exception as e:
        print(f"  {tag} {RED}{label} failed: {e}{RESET}")
    return False


def make_rollout_factory(
    *,
    K: int,
    teacher_kwargs: dict,
    archive: QDArchive,
    max_interventions: int,
    branching: bool,
    max_forks: int,
    max_leaves: int,
    branch_workers: int,
    env_host: str,
):
    def _factory(*, max_steps, timeout, headless, **_kw):
        teacher = TeacherReviewer(**teacher_kwargs)
        agent_cls = BranchingRolloutAgent if branching else RolloutAgent
        kwargs = {}
        if branching:
            kwargs.update(
                max_forks=max_forks,
                max_leaves=max_leaves,
                branch_workers=branch_workers,
                branch_base_port=_kw.get("branch_base_port"),
                env_host=env_host,
            )
        return agent_cls(
            max_steps=max_steps,
            timeout=timeout,
            headless=headless,
            K=K,
            teacher=teacher,
            archive=archive,
            max_interventions=max_interventions,
            **kwargs,
        )
    return _factory


async def worker(
    worker_id: int,
    task_queue: asyncio.Queue,
    results: list,
    results_lock: asyncio.Lock,
    *,
    agent_factory,
    web_app_dir: str,
    run_dir: Path,
    qd_root: Path,
    env_host: str,
    port: int,
    max_steps: int,
    branch_base_port: int | None = None,
):
    server_proc = None
    is_local = env_host in ("localhost", "127.0.0.1")
    server_url = f"http://{env_host}:{port}"
    tag = f"{DIM}[W{worker_id}]{RESET}"

    if is_local:
        server_proc = start_server(web_app_dir, port)
        if not wait_for_server(port, host=env_host):
            if server_proc:
                stop_server(server_proc)
            print(f"  {tag} {RED}Server failed on port {port}{RESET}")
            return

    agent = agent_factory(
        max_steps=max_steps,
        timeout=TASK_TIMEOUT,
        headless=True,
        branch_base_port=branch_base_port,
    )
    try:
        if not await _run_lifecycle_step(
            agent.setup(server_url),
            timeout=AGENT_SETUP_TIMEOUT,
            tag=tag,
            label="Browser setup",
        ):
            return
        print(f"  {tag} ready on :{port}")

        while True:
            try:
                task = task_queue.get_nowait()
            except asyncio.QueueEmpty:
                break

            task_id = task["id"]
            diff = task.get("difficulty", "")
            dc = DIFF_COLOR.get(diff, "")
            task_dir = run_dir / task_id
            _prepare_task_artifacts(task_dir, qd_root, task_id)
            _write_result(
                task_dir,
                _failed_placeholder(
                    task,
                    status="incomplete",
                    message="Task started but did not finish",
                ),
            )

            needs_restart = False
            try:
                result = await asyncio.wait_for(
                    run_task(
                        task=task,
                        agent_runner=agent,
                        server_url=server_url,
                        web_app_dir=web_app_dir,
                        task_dir=task_dir,
                    ),
                    timeout=TASK_TIMEOUT,
                )
                result.pop("status", None)
                result.pop("retryable", None)
                admission = None
                if not result.get("branching"):
                    # QD-archive admission (after hard verifier ran inside run_task)
                    admission = agent.admit_to_archive(
                        task_id=task_id, passed=result["passed"],
                    )
                    if admission is not None:
                        result["qd_admission"] = admission
                        with open(task_dir / "result.json", "w") as f:
                            json.dump(result, f, indent=2)

                badge = (f"{BG_GREEN}{WHITE}{BOLD} PASS {RESET}"
                         if result["passed"]
                         else f"{BG_RED}{WHITE}{BOLD} FAIL {RESET}")
                qd = ""
                if result.get("branching"):
                    qd_count = sum(
                        1 for a in result.get("qd_admissions", [])
                        if a.get("admitted")
                    )
                    qd = (
                        f" {MAGENTA}leaves:{result.get('num_passed_leaves', 0)}/"
                        f"{result.get('num_leaves', 0)} QD:{qd_count}{RESET}"
                    )
                elif admission and admission.get("admitted"):
                    qd = f" {MAGENTA}QD:{admission['bin']}{RESET}"
                teacher_int = result.get(
                    "teacher_interventions",
                    getattr(agent, "_teacher_interventions", 0),
                )
                print(f"  {tag} {BOLD}{task_id}{RESET} {dc}{diff}{RESET}  "
                      f"{badge} {DIM}{result['elapsed']}s {result['steps']} steps"
                      f" int={teacher_int}{RESET}{qd}")
                if result.get("errors"):
                    err_text = " ".join(str(e) for e in result["errors"])
                    if any(k in err_text for k in
                           ("INSUFFICIENT_RESOURCES", "Timeout", "CDP",
                            "consecutive failures")):
                        needs_restart = True
            except asyncio.TimeoutError:
                print(f"  {tag} {BOLD}{task_id}{RESET}  "
                      f"{BG_YELLOW}{WHITE}{BOLD} TIME {RESET}")
                result = _failed_placeholder(
                    task,
                    status="timeout",
                    message=f"Timed out after {TASK_TIMEOUT}s",
                )
                result["elapsed"] = TASK_TIMEOUT
                _write_result(task_dir, result)
                needs_restart = True
            except Exception as e:
                print(f"  {tag} {BOLD}{task_id}{RESET}  "
                      f"{BG_RED}{WHITE}{BOLD} ERR  {RESET} {DIM}{e}{RESET}")
                result = _failed_placeholder(
                    task,
                    status="error",
                    message=f"Agent crashed: {e}",
                )
                result["errors"] = [str(e)]
                _write_result(task_dir, result)
                needs_restart = True

            async with results_lock:
                results.append(result)

            if needs_restart and not task_queue.empty() \
                    and hasattr(agent, "restart_session"):
                if not await _run_lifecycle_step(
                    agent.restart_session(),
                    timeout=AGENT_RESTART_TIMEOUT,
                    tag=tag,
                    label="Restart",
                ):
                    break
    finally:
        await _run_lifecycle_step(
            agent.teardown(),
            timeout=AGENT_TEARDOWN_TIMEOUT,
            tag=tag,
            label="Teardown",
        )
        if server_proc:
            stop_server(server_proc)


async def main():
    parser = argparse.ArgumentParser(
        description="Speculative Rollback Correction rollout runner")
    parser.add_argument("--task-id", default=None)
    parser.add_argument("--difficulty", choices=["easy", "medium", "hard"],
                        default=None)
    parser.add_argument("--max-steps", type=int, default=30)
    parser.add_argument("--workers", type=int, default=4)
    parser.add_argument("--base-port", type=int, default=13001)
    parser.add_argument("--env-host", default="localhost")
    parser.add_argument("--output-dir", default=None)
    parser.add_argument("--web-app", default="webarena_infinity/apps/gmail")
    parser.add_argument("--task-suite", default="real-tasks")
    parser.add_argument("--tag", default=None)
    parser.add_argument("--resume", default=None,
                        help="Resume into an existing rollout run dir: reuse "
                             "the directory, skip tasks that already have a "
                             "result.json, and reuse its qd_archive.")
    parser.add_argument("--retry-stuck", type=int, default=1,
                        help="After the parallel pass, re-run any task whose "
                             "result.json indicates the worker stalled "
                             "(incomplete placeholder, CDP/Connection-refused "
                             "errors, etc.). Timeout results are kept as "
                             "failures. Retries are sequential (single worker) "
                             "for stability. 0 = disable.")

    # Algorithm-specific
    parser.add_argument("--K", type=int, default=3,
                        help="Speculative branch length (student steps before review).")
    parser.add_argument("--max-interventions", type=int, default=6)
    parser.add_argument("--branching", action="store_true",
                        help="Fork rejected student branches into separate logical leaves.")
    parser.add_argument("--max-forks", type=int, default=4,
                        help="Maximum rejected-branch student forks per task.")
    parser.add_argument("--max-leaves", type=int, default=8,
                        help="Maximum logical leaves per task, including the root.")
    parser.add_argument("--branch-workers", type=int, default=4,
                        help="Parallel local env/browser sessions per branching task.")
    parser.add_argument("--teacher-base-url", default=None,
                        help="OpenAI-compatible teacher server (defaults to "
                             "$TEACHER_BASE_URL or http://localhost:9002/v1)")
    parser.add_argument("--teacher-model", default=None,
                        help="Teacher served-model name (defaults to $TEACHER_MODEL)")
    parser.add_argument("--teacher-api-key", default=None)
    parser.add_argument("--teacher-review-context-steps", type=int, default=5,
                        help="Recent pre-branch steps shown to first-shot teacher review "
                             "(default: $TEACHER_REVIEW_CONTEXT_STEPS or 4).")
    parser.add_argument("--teacher-correction-image-max", type=int, default=6,
                        help="Max recent images shown to second-shot teacher correction "
                             "(default: $TEACHER_CORRECTION_IMAGE_MAX or 6).")

    # QD archive
    parser.add_argument("--qd-root", default=None,
                        help="Root dir for QD archive (default: <run_dir>/qd_archive)")
    parser.add_argument("--qd-max-length", type=int, default=60)
    parser.add_argument("--qd-max-repeat", type=int, default=4)

    args = parser.parse_args()

    web_app_dir = str(Path(args.web_app).resolve())
    output_dir = args.output_dir or os.path.join(web_app_dir, "results")

    all_tasks = load_tasks(web_app_dir, task_suite=args.task_suite)
    tasks = filter_tasks(all_tasks, task_id=args.task_id,
                         difficulty=args.difficulty)
    if not tasks:
        print(f"{RED}No tasks matched.{RESET}")
        sys.exit(1)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    suite_tag = f"_{args.task_suite}" if args.task_suite != "real-tasks" else ""
    extra_tag = f"_{args.tag}" if args.tag else ""
    if args.resume:
        run_dir = Path(args.resume).resolve()
        if not run_dir.is_dir():
            print(f"{RED}--resume dir does not exist: {run_dir}{RESET}")
            sys.exit(1)
        # Skip tasks that already completed cleanly. A "clean" task is one
        # whose result.json parses AND is not a Timeout / crash placeholder
        # (those should be retried, not skipped).
        done_ids = set()
        for sub in run_dir.iterdir():
            if not sub.is_dir() or not sub.name.startswith("task_"):
                continue
            rj = sub / "result.json"
            if not rj.is_file():
                continue
            try:
                r = json.loads(rj.read_text())
            except Exception:
                continue
            if r.get("passed") or not _looks_stuck_result(r):
                done_ids.add(sub.name)
        before = len(tasks)
        tasks = [t for t in tasks if t["id"] not in done_ids]
        print(f"{YELLOW}Resume: {len(done_ids)} tasks already done, "
              f"{len(tasks)}/{before} remaining.{RESET}")
        if not tasks:
            print(f"{GREEN}Nothing to do.{RESET}")
            sys.exit(0)
    else:
        # Tagged "rollout" (vs "_parallel" in eval) so logs are easy to spot.
        # Include both student + teacher model slugs so we can tell runs apart.
        def _slug(name: str) -> str:
            n = (name or "").lower()
            for ch in (".", "/", " "):
                n = n.replace(ch, "-")
            return n.strip("-")[:40]
        student_slug = _slug(os.environ.get("QWEN_MODEL", "qwen"))
        teacher_slug = _slug(args.teacher_model
                             or os.environ.get("TEACHER_MODEL", "teacher"))
        run_dir = Path(output_dir) / (
            f"{student_slug}__vs__{teacher_slug}_{timestamp}"
            f"{suite_tag}{extra_tag}_rollout"
        )
        run_dir.mkdir(parents=True, exist_ok=True)

    qd_root = Path(args.qd_root) if args.qd_root else (run_dir / "qd_archive")
    archive = QDArchive(
        qd_root,
        max_length=args.qd_max_length,
        max_repeat=args.qd_max_repeat,
        max_interventions=args.max_interventions,
    )

    teacher_kwargs = dict(
        base_url=args.teacher_base_url,
        model=args.teacher_model,
        api_key=args.teacher_api_key,
        review_context_steps=args.teacher_review_context_steps,
        correction_image_max=args.teacher_correction_image_max,
    )

    agent_factory = make_rollout_factory(
        K=args.K,
        teacher_kwargs=teacher_kwargs,
        archive=archive,
        max_interventions=args.max_interventions,
        branching=args.branching,
        max_forks=args.max_forks,
        max_leaves=args.max_leaves,
        branch_workers=args.branch_workers,
        env_host=args.env_host,
    )

    num_workers = min(args.workers, len(tasks))
    port_hi = args.base_port + num_workers - 1
    branch_span = max(0, args.branch_workers - 1) if args.branching else 0
    branch_port_hi = (
        args.base_port + num_workers + num_workers * branch_span - 1
        if branch_span else port_hi
    )

    print(f"\n{BOLD}{CYAN}{'=' * 60}{RESET}")
    print(f"{BOLD}{CYAN}  Speculative Rollback Rollout{RESET}")
    print(f"{BOLD}{CYAN}{'=' * 60}{RESET}")
    print(f"  {DIM}Suite:{RESET}   {BOLD}{args.task_suite}{RESET}")
    print(f"  {DIM}App:{RESET}     {BOLD}{args.web_app}{RESET}")
    print(f"  {DIM}Tasks:{RESET}   {BOLD}{len(tasks)}{RESET}")
    print(f"  {DIM}Workers:{RESET} {BOLD}{num_workers}{RESET}  "
          f"{DIM}K:{RESET} {BOLD}{args.K}{RESET}  "
          f"{DIM}Max-int:{RESET} {BOLD}{args.max_interventions}{RESET}")
    if args.branching:
        print(f"  {DIM}Branching:{RESET} {BOLD}on{RESET}  "
              f"{DIM}Max-forks:{RESET} {BOLD}{args.max_forks}{RESET}  "
              f"{DIM}Max-leaves:{RESET} {BOLD}{args.max_leaves}{RESET}  "
              f"{DIM}Branch-workers:{RESET} {BOLD}{args.branch_workers}{RESET}")
    print(f"  {DIM}Env:{RESET}     {args.env_host}:{args.base_port}-{port_hi}")
    if branch_span:
        print(f"  {DIM}Branch env:{RESET} {args.env_host}:"
              f"{args.base_port + num_workers}-{branch_port_hi}")
    print(f"  {DIM}Teacher:{RESET} {teacher_kwargs.get('base_url') or os.environ.get('TEACHER_BASE_URL', 'http://localhost:9002/v1')}"
          f"  model={teacher_kwargs.get('model') or os.environ.get('TEACHER_MODEL', 'Qwen3.6-27B')}")
    print(f"  {DIM}Output:{RESET}  {run_dir}")
    print(f"  {DIM}QD root:{RESET} {qd_root}")
    print(f"{CYAN}{'─' * 60}{RESET}\n")

    task_queue: asyncio.Queue = asyncio.Queue()
    for t in tasks:
        await task_queue.put(t)
    results: list = []
    results_lock = asyncio.Lock()

    async def staggered_worker(i, delay):
        if delay > 0:
            await asyncio.sleep(delay)
        branch_base_port = (
            args.base_port + num_workers + i * branch_span
            if branch_span else None
        )
        await worker(
            worker_id=i,
            task_queue=task_queue,
            results=results,
            results_lock=results_lock,
            agent_factory=agent_factory,
            web_app_dir=web_app_dir,
            run_dir=run_dir,
            qd_root=qd_root,
            env_host=args.env_host,
            port=args.base_port + i,
            max_steps=args.max_steps,
            branch_base_port=branch_base_port,
        )

    STAGGER = 5
    await asyncio.gather(*[staggered_worker(i, i * STAGGER)
                           for i in range(num_workers)])

    # ----- Retry pass: re-run "stuck" tasks sequentially -----
    # A stuck task is one that didn't run to completion under its own
    # power because the browser/LLM process failed or the runner was
    # killed externally. Hard task timeouts are kept as failed results;
    # those trajectories are discarded instead of retried.
    if args.retry_stuck > 0:
        all_task_dict = {t["id"]: t for t in tasks}
        # Index whatever results we have so far.
        latest = {r["task_id"]: r for r in results}

        def _is_stuck(tid: str) -> bool:
            r = latest.get(tid)
            if r is None:
                # No in-memory result: check disk (resume / earlier crash).
                rj = run_dir / tid / "result.json"
                if not rj.is_file():
                    return True  # never produced a result
                try:
                    r = json.loads(rj.read_text())
                except Exception:
                    return True
            return _looks_stuck_result(r)

        for retry_round in range(args.retry_stuck):
            stuck_tids = [tid for tid in all_task_dict if _is_stuck(tid)]
            if not stuck_tids:
                break
            print(f"\n{YELLOW}Retry round {retry_round + 1}: "
                  f"{len(stuck_tids)} stuck tasks → "
                  f"sequential re-run ({', '.join(stuck_tids)}){RESET}")
            for tid in stuck_tids:
                # Wipe the prior task dir so the retry is a clean attempt.
                td = run_dir / tid
                if td.is_dir():
                    shutil.rmtree(td)
                retry_q: asyncio.Queue = asyncio.Queue()
                await retry_q.put(all_task_dict[tid])
                retry_results: list = []
                retry_lock = asyncio.Lock()
                await worker(
                    worker_id=0,
                    task_queue=retry_q,
                    results=retry_results,
                    results_lock=retry_lock,
                    agent_factory=agent_factory,
                    web_app_dir=web_app_dir,
                    run_dir=run_dir,
                    qd_root=qd_root,
                    env_host=args.env_host,
                    port=args.base_port,
                    max_steps=args.max_steps,
                    branch_base_port=(
                        args.base_port + 1 if branch_span else None
                    ),
                )
                if retry_results:
                    latest[tid] = retry_results[0]

        # Replace any in-memory results that were stuck/missing with
        # whatever we have on disk now.
        results = list(latest.values())
        # Pick up any tasks that only exist on disk (resume case).
        for sub in sorted(run_dir.iterdir()):
            if not sub.is_dir() or not sub.name.startswith("task_"):
                continue
            tid = sub.name
            if tid in {r["task_id"] for r in results}:
                continue
            rj = sub / "result.json"
            if rj.is_file():
                try:
                    results.append(json.loads(rj.read_text()))
                except Exception:
                    pass

    if not results:
        print(f"{RED}No tasks completed.{RESET}")
        sys.exit(1)

    # When resuming, merge previously-completed task results from disk so
    # the aggregate report covers the whole suite.
    if args.resume:
        existing_ids = {r["task_id"] for r in results}
        for sub in sorted(run_dir.iterdir()):
            if not sub.is_dir() or not sub.name.startswith("task_"):
                continue
            tid = sub.name
            if tid in existing_ids:
                continue
            rj = sub / "result.json"
            if not rj.is_file():
                continue
            try:
                results.append(json.loads(rj.read_text()))
            except Exception:
                pass

    results.sort(key=lambda r: r["task_id"])
    total = len(results)
    passed = sum(1 for r in results if r["passed"])
    by_diff: dict[str, dict] = {}
    for r in results:
        d = r.get("difficulty", "")
        if d:
            by_diff.setdefault(d, {"total": 0, "passed": 0})
            by_diff[d]["total"] += 1
            if r["passed"]:
                by_diff[d]["passed"] += 1

    aggregate = {
        "model": "qwen-rollout",
        "K": args.K,
        "branching": args.branching,
        "max_forks": args.max_forks if args.branching else 0,
        "max_leaves": args.max_leaves if args.branching else 1,
        "branch_workers": args.branch_workers if args.branching else 1,
        "timestamp": timestamp,
        "workers": num_workers,
        "total": total,
        "passed": passed,
        "pass_rate": round(passed / total * 100, 1) if total else 0,
        "by_difficulty": by_diff,
        "qd_root": str(qd_root),
        "tasks": results,
    }
    with open(run_dir / "results.json", "w") as f:
        json.dump(aggregate, f, indent=2)

    report_path = generate_report(results, "qwen-rollout", timestamp, run_dir)

    pct = aggregate["pass_rate"]
    pct_color = GREEN if pct >= 50 else RED
    print(f"\n{BOLD}{CYAN}{'=' * 60}{RESET}")
    print(f"  {BOLD}Rollout: {pct_color}{passed}/{total} passed ({pct}%){RESET}")
    print()
    for d in ["easy", "medium", "hard"]:
        if d in by_diff:
            info = by_diff[d]
            dc = DIFF_COLOR.get(d, "")
            rc = GREEN if info["passed"] == info["total"] else (
                YELLOW if info["passed"] > 0 else RED)
            print(f"    {dc}{d.capitalize():8s}{RESET} "
                  f"{rc}{info['passed']}/{info['total']}{RESET}")
    print()
    print(f"  {DIM}Report:{RESET}   {MAGENTA}{report_path}{RESET}")
    print(f"  {DIM}QD root:{RESET}  {MAGENTA}{qd_root}{RESET}")
    print(f"{CYAN}{'=' * 60}{RESET}\n")


if __name__ == "__main__":
    asyncio.run(main())
