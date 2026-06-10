"""Task loading, filtering, verification, and single-task execution."""

import importlib.util
import asyncio
import json
import os
import time
from pathlib import Path

import requests

from agents import AgentResult

TASK_TIMEOUT = 600  # seconds per task wall-clock limit
RESET_TIMEOUT = float(os.environ.get("TASK_RESET_TIMEOUT", "15"))
VERIFY_TIMEOUT = float(os.environ.get("TASK_VERIFY_TIMEOUT", "60"))


def load_tasks(web_app_dir: str, task_suite: str = "real-tasks") -> list[dict]:
    with open(Path(web_app_dir) / f"{task_suite}.json") as f:
        return json.load(f)


def filter_tasks(
    tasks: list[dict],
    task_id: str | None = None,
    difficulty: str | None = None,
) -> list[dict]:
    if task_id:
        ids = [s.strip() for s in task_id.split(",")]
        return [t for t in tasks if t["id"] in ids]
    if difficulty:
        return [t for t in tasks if t.get("difficulty") == difficulty]
    return tasks


def load_verifier(web_app_dir: str, verify_path: str):
    full_path = str(Path(web_app_dir) / verify_path)
    spec = importlib.util.spec_from_file_location("verifier", full_path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod.verify


def reset_state(server_url: str):
    resp = requests.post(f"{server_url}/api/reset", timeout=RESET_TIMEOUT)
    resp.raise_for_status()
    time.sleep(0.5)


async def run_task(
    task: dict,
    agent_runner,
    server_url: str,
    web_app_dir: str,
    task_dir: Path,
) -> dict:
    """Reset state, run the agent, verify, return result dict."""
    task_id = task["id"]

    # 1. Reset
    await asyncio.to_thread(reset_state, server_url)

    if hasattr(agent_runner, "run_with_verifier"):
        try:
            verify_fn = load_verifier(web_app_dir, task["verify"])
        except Exception as e:
            def verify_fn(_server_url, _err=e):
                return False, f"Verifier load exception: {_err}"

        task_result = await agent_runner.run_with_verifier(
            task=task,
            server_url=server_url,
            web_app_dir=web_app_dir,
            task_dir=task_dir,
            verify_fn=verify_fn,
        )
        with open(task_dir / "result.json", "w") as f:
            json.dump(task_result, f, indent=2)
        return task_result

    # 2. Run agent
    result: AgentResult = await agent_runner.run(
        task=task["instruction"],
        server_url=server_url,
        task_dir=task_dir,
    )

    # 3. Verify
    try:
        verify_fn = load_verifier(web_app_dir, task["verify"])
        passed, verifier_message = await asyncio.wait_for(
            asyncio.to_thread(verify_fn, server_url),
            timeout=VERIFY_TIMEOUT,
        )
    except asyncio.TimeoutError:
        passed, verifier_message = (
            False,
            f"Verifier timed out after {VERIFY_TIMEOUT:g}s",
        )
    except Exception as e:
        passed, verifier_message = False, f"Verifier exception: {e}"

    task_result = {
        "task_id": task_id,
        "difficulty": task.get("difficulty", ""),
        "instruction": task["instruction"],
        "passed": passed,
        "verifier_message": verifier_message,
        "elapsed": result.elapsed,
        "steps": result.steps,
        "is_done": result.is_done,
        "final_result": result.final_result,
        "errors": result.errors,
    }

    with open(task_dir / "result.json", "w") as f:
        json.dump(task_result, f, indent=2)

    return task_result
