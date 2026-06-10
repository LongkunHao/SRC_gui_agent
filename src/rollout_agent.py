"""Speculative Rollback Correction rollout agent.

Wraps the existing ``Qwen35VLAgent`` (the SFT student) and runs the
algorithm described in the paper:

    1. Student rolls out a K-step speculative branch.
    2. Teacher reviews the branch and either accepts it, or rolls back
       to the earliest harmful step and supplies a corrective action.
    3. The environment replays the accepted prefix and applies the
       correction by:
         - calling /api/reset on the env server
         - re-loading the seed page
         - replaying every executed action from step 0 up to (rollback_to)
         - applying the teacher correction
    4. After the episode the hard verifier (run_eval_parallel calls it)
       decides success.
    5. Verifier-pass trajectories that satisfy quality gates enter the
       per-task QD archive, organised by (length, dominant action,
       teacher-intervention count).

"""

from __future__ import annotations

import asyncio
import base64
import copy
import json
import os
import re
import time
from dataclasses import dataclass, field
from typing import Callable
from pathlib import Path

import requests

from agents import AgentResult
from llm_trace import LLMTracer
from teacher_review import (
    BranchStep,
    ReviewContextStep,
    TeacherDecision,
    TeacherReviewer,
)
from qd_archive import QDArchive
from vision_agents import Qwen35VLAgent, _QWEN_SYSTEM_PROMPT, _QWEN_COLLAPSED_TEXT


_TEACHER_CORRECTION_PROMPT_PATH = Path(
    os.environ.get(
        "TEACHER_CORRECTION_PROMPT_PATH",
        Path(__file__).parent / "prompts" / "teacher_correction_prompt.md",
    )
)

BRANCH_AGENT_SETUP_TIMEOUT = float(
    os.environ.get("ROLLOUT_BRANCH_AGENT_SETUP_TIMEOUT", "75")
)
BRANCH_AGENT_TEARDOWN_TIMEOUT = float(
    os.environ.get("ROLLOUT_BRANCH_AGENT_TEARDOWN_TIMEOUT", "30")
)
BRANCH_TASK_CANCEL_TIMEOUT = float(
    os.environ.get("ROLLOUT_BRANCH_TASK_CANCEL_TIMEOUT", "30")
)


def _load_teacher_correction_prompt_template() -> str:
    return _TEACHER_CORRECTION_PROMPT_PATH.read_text(encoding="utf-8").strip()


def _render_teacher_correction_prompt(
    *,
    task: str,
    server_url: str,
    rollback_reason: str,
    previous_actions: str,
) -> str:
    prompt = _load_teacher_correction_prompt_template()
    values = {
        "task": task,
        "server_url": server_url,
        "rollback_reason": rollback_reason or "(no reason given)",
        "previous_actions": previous_actions,
    }
    for key, value in values.items():
        prompt = prompt.replace(f"{{{{{key}}}}}", value)
    return prompt


# ---------------------------------------------------------------------------
# Helper: build a synthetic Qwen-style assistant response from a teacher
# correction so that it can be appended to the student's history exactly
# the way a normal student step would be.
# ---------------------------------------------------------------------------

def _correction_to_xml(corr: dict) -> tuple[str, str, list[dict]]:
    """Convert a teacher correction params dict into:
        (synthetic_assistant_text, action_summary, list_of_action_dicts)

    The synthetic_assistant_text uses the same <tool_call><function=
    computer_use>...</function></tool_call> XML schema the student emits,
    so it can be transparently inserted into the Qwen agent's
    self._responses list.
    """
    # Build XML tool_call mirroring student's grammar.
    parts = []
    for k, v in corr.items():
        if isinstance(v, (list, dict)):
            v_str = json.dumps(v)
        else:
            v_str = str(v)
        parts.append(f"<parameter={k}>\n{v_str}\n</parameter>")
    xml = (
        "Action: teacher correction.\n"
        "<tool_call>\n<function=computer_use>\n"
        + "\n".join(parts)
        + "\n</function>\n</tool_call>"
    )
    summary = f"teacher: {corr.get('action', 'unknown')}"
    return xml, summary, []  # action dicts filled in by caller after parsing


@dataclass
class _ForkLeafState:
    """Serializable logical rollout session for branching SRC."""

    leaf_id: str
    parent_id: str | None = None
    role: str = "root"
    fork_reason: str = ""
    is_done: bool = False
    final_result: str | None = None
    discarded: bool = False
    discard_reason: str = ""
    executed_per_step: list[list[dict]] = field(default_factory=list)
    screenshots_b64: list[str] = field(default_factory=list)
    responses: list[str] = field(default_factory=list)
    action_summaries: list[str] = field(default_factory=list)
    folded_prefix_k: int = 0
    history: list[dict] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)
    teacher_decisions: list[dict] = field(default_factory=list)
    teacher_interventions: int = 0
    rollback_target_hits: dict[int, int] = field(default_factory=dict)
    branch_records: list[dict] = field(default_factory=list)

    @property
    def steps(self) -> int:
        return len(self.executed_per_step)


@dataclass
class _ForkCoordinator:
    """Shared counters across parallel leaf-worker agents."""

    max_forks: int
    max_leaves: int
    leaf_counter: int = 0
    forks_used: int = 0
    global_branch_no: int = 0


class RolloutAgent(Qwen35VLAgent):
    """Student + Teacher segment-level rollback correction agent.

    Inherits from ``Qwen35VLAgent`` so screenshot capture, prompting,
    coordinate conversion and tool-call parsing are reused.  We override
    the agent loop (``_run_agent_loop``) to interleave K-step branches
    with teacher review and replay-based rollback.
    """

    def __init__(
        self,
        *,
        max_steps: int = 50,
        timeout: int = 600,
        headless: bool = True,
        K: int = 3,
        teacher: TeacherReviewer | None = None,
        archive: QDArchive | None = None,
        max_interventions: int = 6,
        **kw,
    ):
        super().__init__(max_steps=max_steps, timeout=timeout, headless=headless, **kw)
        self.K = K
        self.teacher = teacher or TeacherReviewer()
        self.archive = archive
        self.max_interventions = max_interventions

        # Filled in per task — the canonical replay log.
        self._executed_per_step: list[list[dict]] = []
        self._teacher_decisions: list[dict] = []
        self._teacher_interventions: int = 0

    # ------------------------------------------------------------------ helpers

    async def _reset_env_and_replay(
        self,
        prefix_actions: list[list[dict]],
    ) -> None:
        """Fallback rollback: /api/reset + replay every prior action.

        Used only when the app does not support /api/restore snapshots.
        """
        try:
            await asyncio.to_thread(
                requests.post, f"{self._server_url}/api/reset", timeout=15,
            )
        except Exception as e:
            self._live_errors.append(f"reset error during rollback: {e}")
        try:
            await self._page.goto(self._server_url,
                                  wait_until="domcontentloaded",
                                  timeout=15000)
        except Exception as e:
            self._live_errors.append(f"goto error during rollback: {e}")
        for _ in range(10):
            try:
                r = await asyncio.to_thread(
                    requests.get, f"{self._server_url}/api/state", timeout=5,
                )
                if r.status_code == 200 and r.json():
                    break
            except Exception:
                pass
            await asyncio.sleep(0.5)
        for step_actions in prefix_actions:
            for a in step_actions:
                t = a.get("type")
                if t == "terminate":
                    # terminate is a no-op for replay. Note: hover/move
                    # ARE replayed because many sites expand menus, show
                    # hidden buttons, or change clickable regions on hover
                    # — skipping them would diverge state silently.
                    continue
                try:
                    await asyncio.wait_for(self.execute_action(a),
                                           timeout=20)
                except Exception as e:
                    self._live_errors.append(f"replay error: {e}")

    async def _rollback_to(self, new_total: int) -> None:
        """Roll the env back so the next action will be step ``new_total``.

        We always use reset-and-replay: POST /api/reset then re-execute
        every prior student action.
        """
        await self._reset_env_and_replay(self._executed_per_step[:new_total])

    def _truncate_state(self, n_steps: int) -> None:
        """Keep only the first ``n_steps`` of the agent's running state."""
        del self._screenshots_b64[n_steps:]
        del self._responses[n_steps:]
        del self._action_summaries[n_steps:]
        del self._executed_per_step[n_steps:]
        # _prepare_step folds the screenshot history using _folded_prefix_k.
        # If we don't clamp it here, after a rollback it can exceed the
        # remaining history length and cause the current screenshot to be
        # collapsed away in the next prompt.
        if hasattr(self, "_folded_prefix_k"):
            self._folded_prefix_k = min(self._folded_prefix_k, n_steps)

    def _teacher_review_context(self, branch_start: int) -> list[ReviewContextStep]:
        """Recent pre-branch observations for first-shot teacher review."""
        n = max(0, int(getattr(self.teacher, "review_context_steps", 0) or 0))
        if n <= 0 or branch_start <= 0:
            return []
        start = max(0, branch_start - n)
        ctx: list[ReviewContextStep] = []
        for abs_step in range(start, branch_start):
            if abs_step >= len(self._screenshots_b64):
                continue
            actions = (
                list(self._executed_per_step[abs_step])
                if abs_step < len(self._executed_per_step)
                else []
            )
            summary = (
                self._action_summaries[abs_step]
                if abs_step < len(self._action_summaries)
                else ""
            )
            ctx.append(ReviewContextStep(
                absolute_step=abs_step,
                screenshot_b64=self._screenshots_b64[abs_step],
                action_summary=summary,
                action_dicts=actions,
            ))
        return ctx

    def _build_qwen_correction_messages(
        self,
        *,
        task: str,
        server_url: str,
        current_screenshot_b64: str,
        rollback_reason: str,
        image_max: int = 6,
    ) -> list[dict]:
        """Build a Qwen-format messages list for the second-shot teacher.

        Mirrors ``Qwen35VLAgent._prepare_step``:
          - same ``_QWEN_SYSTEM_PROMPT``
          - same per-step user/assistant interleaving
          - same image-folding rule with a larger configurable image window
          - the *current* observation is the post-rollback screenshot
            and the instruction is augmented with the rollback reason
        so the teacher behaves like a stronger student that knows why the
        previous attempt was discarded.
        """
        # Compose previous-actions summary (same shape as the student's
        # _prepare_step prev_str).
        prev = [
            f"Step {i + 1}: {self._action_summaries[i]}"
            for i in range(len(self._action_summaries))
        ]
        prev_str = "\n".join(prev) if prev else "None"

        instruction_prompt = _render_teacher_correction_prompt(
            task=task,
            server_url=server_url,
            rollback_reason=rollback_reason,
            previous_actions=prev_str,
        )

        # Snapshot the per-step screenshots; the post-rollback shot is the
        # observation for the upcoming (yet-to-execute) step.
        all_imgs = list(self._screenshots_b64) + [current_screenshot_b64]
        total = len(all_imgs)
        # Folding: keep at most ``image_max`` un-collapsed observations.
        # The previous chunk-fold logic could collapse far too many images
        # (e.g. with image_max=10 and total=11 it would fold 10 of 11);
        # this fold-the-oldest-N rule keeps exactly the last image_max.
        folded_prefix_k = max(0, total - image_max)
        # Truncate to last history_n steps (reuse student's setting).
        start_step = max(1, total - self._history_n)

        messages: list[dict] = [
            {"role": "system",
             "content": [{"type": "text", "text": _QWEN_SYSTEM_PROMPT}]},
        ]

        for s in range(start_step, total + 1):
            is_first = (s == start_step)
            is_collapsed = (s <= folded_prefix_k)

            if is_collapsed:
                if is_first:
                    user_content = [
                        {"type": "text", "text": instruction_prompt}
                    ]
                else:
                    user_content = [
                        {"type": "text", "text": "<tool_response>\n"},
                        {"type": "text", "text": _QWEN_COLLAPSED_TEXT},
                        {"type": "text", "text": "\n</tool_response>"},
                    ]
            else:
                img_url = f"data:image/png;base64,{all_imgs[s - 1]}"
                if is_first:
                    user_content = [
                        {"type": "image_url", "image_url": {"url": img_url}},
                        {"type": "text", "text": instruction_prompt},
                    ]
                else:
                    user_content = [
                        {"type": "text", "text": "<tool_response>\n"},
                        {"type": "image_url", "image_url": {"url": img_url}},
                        {"type": "text", "text": "\n</tool_response>"},
                    ]

            messages.append({"role": "user", "content": user_content})

            # Past assistant responses (for steps already executed).
            if s <= total - 1 and (s - 1) < len(self._responses):
                messages.append({
                    "role": "assistant",
                    "content": [
                        {"type": "text", "text": self._responses[s - 1]}
                    ],
                })

        return messages

    async def _request_teacher_correction(
        self,
        *,
        task: str,
        server_url: str,
        current_screenshot_b64: str,
        rollback_reason: str,
    ) -> tuple[list[dict], list[dict], str]:
        """Ask the teacher for one Qwen-schema corrective step."""
        msgs = self._build_qwen_correction_messages(
            task=task,
            server_url=server_url,
            current_screenshot_b64=current_screenshot_b64,
            rollback_reason=rollback_reason,
            image_max=getattr(self.teacher, "correction_image_max", 6),
        )
        corr_xml = await self.teacher.review_correction(messages=msgs)
        corrections: list[dict] = []
        actions: list[dict] = []
        # Parse EVERY <tool_call>...</tool_call> block. Some teacher
        # outputs chain calls; picking only the first silently drops actions.
        for tc in re.finditer(r"<tool_call>(.*?)</tool_call>", corr_xml, re.DOTALL):
            params = self._parse_xml_tool_call(tc.group(1))
            if not params:
                continue
            corrections.append(params)
            actions.extend(self._tool_params_to_actions(params))
        return corrections, actions, corr_xml

    async def _execute_teacher_actions(
        self,
        actions: list[dict],
        *,
        errors: list[str],
        server_url: str,
        verify_fn: Callable[[str], tuple[bool, str]] | None = None,
        verifier_target: dict | None = None,
        verifier_key: str = "correction_terminate_verifier",
    ) -> tuple[bool, str | None]:
        """Execute teacher actions; only allow terminate through verifier."""
        for a in actions:
            if a.get("type") == "terminate":
                if verify_fn is not None:
                    try:
                        v_passed, v_msg = await asyncio.to_thread(
                            verify_fn, server_url
                        )
                    except Exception as e:
                        v_passed, v_msg = False, f"Verifier exception: {e}"
                    feedback = {"passed": v_passed, "message": v_msg}
                    if verifier_target is not None:
                        verifier_target[verifier_key] = feedback
                    if not v_passed:
                        errors.append(
                            "teacher correction terminate rejected by hard "
                            f"verifier: {v_msg}"
                        )
                        continue
                return True, "teacher terminated"
            try:
                await self.execute_action(a)
            except Exception as e:
                errors.append(f"corr exec error: {e}")
        return False, None

    # ------------------------------------------------------------------ loop

    async def _run_agent_loop(
        self,
        task: str,
        server_url: str,
        task_dir: Path,
        screenshots_dir: Path,
    ) -> dict:
        """K-step branches + teacher review + rollback. Overrides base."""
        history = self._live_history
        errors = self._live_errors
        is_done = False
        final_result = None

        # Per-task state
        self._executed_per_step = []
        self._teacher_decisions = []
        self._teacher_interventions = 0
        # Share the per-task LLM tracer (created by base run()) with the
        # teacher so its first-shot review and second-shot correction
        # calls also land in {task_dir}/llm_calls.jsonl.
        if self.teacher is not None and getattr(self, "_tracer", None) is not None:
            self.teacher.tracer = self._tracer
        # Track repeated rollback targets to break out of teacher-loop where
        # the teacher keeps rolling back to the same step with an ineffective
        # correction (e.g. scroll amount=1 no-op).
        self._rollback_target_hits: dict[int, int] = {}
        # Per-branch screenshot tracking. Without this, step_{idx}.png gets
        # overwritten every time we roll back and re-attempt, losing the
        # visual record of rejected branches. We also track rollback-verify
        # screenshots for human inspection.
        self._branch_records: list[dict] = []
        self._init_conversation(task, server_url)

        # Soft failure budget within the speculative loop (mirrors the
        # base agent's own consecutive_failures / empty_output_count logic
        # so a stuck student doesn't burn the entire step budget on
        # zero-action steps).
        consecutive_failures = 0
        empty_output_count = 0

        branch_no = 0  # 1-based ID of the current speculative branch
        step = 0  # absolute step counter
        while step < self.max_steps:
            if consecutive_failures >= self.max_consecutive_failures:
                errors.append(
                    f"Stopping after {consecutive_failures} consecutive failures")
                break

            # ----- 1. Student executes up to K speculative steps -----
            branch_start = step
            branch_history_start = len(history)
            branch_no += 1
            branch: list[BranchStep] = []
            branch_done = False  # student emitted terminate inside branch
            pending_done_text: str | None = None
            empty_takeover_handled = False
            branch_step_imgs: list[str] = []
            branch_thoughts: list[str] = []
            branch_actions: list[list[dict]] = []
            for _ in range(self.K):
                if step >= self.max_steps:
                    break
                if not await self._check_browser_health():
                    errors.append(f"Browser unrecoverable at step {step}")
                    return {"steps": step, "is_done": False,
                            "final_result": None, "errors": errors,
                            "history": history}

                screenshot = await self.take_screenshot()
                ss_path = screenshots_dir / f"step_{step}.png"
                ss_path.write_bytes(screenshot)
                # Also save under a non-clobbering per-branch name so the
                # viz can still show this attempt after a rollback overwrites
                # the canonical step_{step}.png file.
                bs_name = f"b{branch_no}_s{len(branch)}.png"
                (screenshots_dir / bs_name).write_bytes(screenshot)
                branch_step_imgs.append(bs_name)
                # Register with the per-task LLM tracer so this exact
                # screenshot is referenced by path (not re-encoded inline)
                # in llm_calls.jsonl.
                tracer = getattr(self, "_tracer", None)
                if tracer is not None:
                    tracer.register(screenshot, ss_path)

                self._prepare_step(step, screenshot)
                response, api_err = await self._call_with_retry()
                if api_err:
                    errors.append(f"Student API error at step {step}: {api_err}")
                    consecutive_failures += 1
                    break

                result = self._parse_response(response)

                # Empty-output handling (mirrors base loop). _prepare_step
                # has already pushed a screenshot and a response; if the
                # student returned nothing usable we drop those bookkeeping
                # entries and skip the branch step.
                if (not result.actions and not result.is_done
                        and not result.action_descriptions):
                    empty_output_count += 1
                    consecutive_failures += 1
                    # Roll back the in-memory state pushed by _prepare_step
                    # so the prompt stays aligned with the executed log.
                    if len(self._screenshots_b64) > len(self._executed_per_step):
                        self._screenshots_b64.pop()
                    if len(self._responses) > len(self._executed_per_step):
                        self._responses.pop()
                    if len(self._action_summaries) > len(self._executed_per_step):
                        self._action_summaries.pop()
                    if empty_output_count >= 3:
                        reason = (
                            "student produced 3 consecutive empty outputs; "
                            "teacher taking over current state"
                        )
                        errors.append(reason)
                        b64 = base64.b64encode(screenshot).decode()
                        if self._teacher_interventions >= self.max_interventions:
                            reason_budget = (
                                "max teacher interventions reached during "
                                "empty-output fallback; discarding trajectory"
                            )
                            errors.append(reason_budget)
                            self._branch_records.append({
                                "branch_no": branch_no,
                                "branch_start": branch_start,
                                "branch_len": 0,
                                "step_imgs": list(branch_step_imgs),
                                "thoughts": [],
                                "actions": [],
                                "post_img": (
                                    branch_step_imgs[-1]
                                    if branch_step_imgs else None
                                ),
                                "accepted": False,
                                "rollback_to": branch_start,
                                "reason": reason,
                                "empty_output_fallback": True,
                                "discarded": True,
                                "discard_reason": reason_budget,
                                "correction": None,
                                "correction_raw": "",
                            })
                            self._teacher_decisions.append({
                                "accept": False,
                                "rollback_to": branch_start,
                                "reason": reason,
                                "raw": "",
                                "branch_start": branch_start,
                                "branch_len": 0,
                                "branch_no": branch_no,
                                "empty_output_fallback": True,
                                "discarded": True,
                                "discard_reason": reason_budget,
                            })
                            return {"steps": step, "is_done": False,
                                    "final_result": None, "errors": errors,
                                    "history": history}
                        corrections: list[dict] = []
                        actions: list[dict] = []
                        corr_xml = ""
                        try:
                            corrections, actions, corr_xml = (
                                await self._request_teacher_correction(
                                    task=task,
                                    server_url=server_url,
                                    current_screenshot_b64=b64,
                                    rollback_reason=reason,
                                )
                            )
                        except Exception as e:
                            errors.append(f"empty-output teacher error: {e}")

                        branch_record = {
                            "branch_no": branch_no,
                            "branch_start": branch_start,
                            "branch_len": 0,
                            "step_imgs": list(branch_step_imgs),
                            "thoughts": [],
                            "actions": [],
                            "post_img": branch_step_imgs[-1] if branch_step_imgs else None,
                            "accepted": False,
                            "rollback_to": branch_start,
                            "reason": reason,
                            "empty_output_fallback": True,
                            "correction": corrections or None,
                            "correction_raw": corr_xml[:2000],
                        }

                        if actions:
                            self._screenshots_b64.append(b64)
                            first_corr = corrections[0] if corrections else {}
                            self._responses.append(
                                corr_xml or _correction_to_xml(first_corr)[0]
                            )
                            self._action_summaries.append(
                                "teacher: " + ", ".join(
                                    c.get("action", "unknown")
                                    for c in corrections
                                )
                            )
                            self._executed_per_step.append(list(actions))
                            history.append({
                                "step": step,
                                "phase": "teacher_correction",
                                "branch_no": branch_no,
                                "correction": corrections,
                                "actions": actions,
                                "reason": reason,
                                "empty_output_fallback": True,
                            })
                            done, done_text = await self._execute_teacher_actions(
                                actions,
                                errors=errors,
                                server_url=server_url,
                            )
                            if done:
                                is_done = True
                                final_result = done_text
                            step += 1
                            self._teacher_interventions += 1
                            self._branch_records.append(branch_record)
                            self._teacher_decisions.append({
                                "accept": False,
                                "rollback_to": branch_start,
                                "reason": reason,
                                "raw": corr_xml[:2000],
                                "branch_start": branch_start,
                                "branch_len": 0,
                                "branch_no": branch_no,
                                "empty_output_fallback": True,
                                "correction": corrections or None,
                            })
                            consecutive_failures = 0
                            empty_output_count = 0
                            empty_takeover_handled = True
                            break

                        reason_no_action = (
                            "empty-output fallback teacher returned no "
                            "executable correction"
                        )
                        errors.append(reason_no_action)
                        branch_record["discarded"] = True
                        branch_record["discard_reason"] = reason_no_action
                        self._teacher_interventions += 1
                        self._branch_records.append(branch_record)
                        self._teacher_decisions.append({
                            "accept": False,
                            "rollback_to": branch_start,
                            "reason": reason,
                            "raw": corr_xml[:2000],
                            "branch_start": branch_start,
                            "branch_len": 0,
                            "branch_no": branch_no,
                            "empty_output_fallback": True,
                            "discarded": True,
                            "discard_reason": reason_no_action,
                            "correction": corrections or None,
                        })
                        return {"steps": step, "is_done": False,
                                "final_result": None, "errors": errors,
                                "history": history}
                    continue

                consecutive_failures = 0
                empty_output_count = 0

                # _parse_response already appended to _screenshots_b64 (via
                # _prepare_step), _responses and _action_summaries.
                # Track executed actions for replay.
                actions_this_step = list(result.actions)
                self._executed_per_step.append(actions_this_step)
                branch_thoughts.append((result.text or "")[:2000])
                branch_actions.append(actions_this_step)

                step_record = {
                    "step": step,
                    "phase": "student_branch",
                    "branch_start": branch_start,
                    "branch_no": branch_no,
                    "thought": result.text,
                    "actions": actions_this_step,
                }
                history.append(step_record)

                # Build BranchStep BEFORE executing (screenshot is what student saw)
                branch.append(BranchStep(
                    index_in_branch=len(branch) - 0,
                    screenshot_b64=base64.b64encode(screenshot).decode(),
                    thought=result.text or "",
                    action_summary=(self._action_summaries[-1] if self._action_summaries else ""),
                    action_dicts=actions_this_step,
                ))

                # Execute (terminate is a special pseudo-action).
                # NOTE: defer setting is_done until the teacher actually
                # accepts this branch — otherwise a teacher-rollback that
                # discards a premature terminate would still cause the
                # outer loop to exit immediately.
                if result.is_done:
                    branch_done = True
                    pending_done_text = result.text
                    step += 1
                    break

                await self._execute_step(step, result)
                self._on_step_done(step, result, screenshot)
                step += 1

            if empty_takeover_handled:
                if is_done:
                    break
                continue

            if not branch:
                # No usable student steps in this branch (e.g. all empty).
                # Outer loop will retry until consecutive_failures budget
                # is hit.
                if is_done:
                    break
                continue

            # ----- 2. Teacher review of the branch -----
            post_branch_ss = await self.take_screenshot()
            post_name = f"branch_{branch_start}_post.png"
            (screenshots_dir / post_name).write_bytes(post_branch_ss)
            # Also pin under a per-branch-no name to survive overwrites.
            post_name_unique = f"b{branch_no}_post.png"
            (screenshots_dir / post_name_unique).write_bytes(post_branch_ss)
            tracer = getattr(self, "_tracer", None)
            if tracer is not None:
                tracer.register(post_branch_ss,
                                screenshots_dir / post_name_unique)
            decision: TeacherDecision = await self.teacher.review(
                task=task,
                server_url=server_url,
                branch_start=branch_start,
                branch=branch,
                post_branch_screenshot_b64=base64.b64encode(post_branch_ss).decode(),
                accepted_prefix=self._teacher_review_context(branch_start),
            )

            # Stash this branch's record (regardless of accept/reject) so
            # the visualizer can show every attempt.
            branch_record = {
                "branch_no": branch_no,
                "branch_start": branch_start,
                "branch_len": len(branch),
                "step_imgs": list(branch_step_imgs),
                "thoughts": list(branch_thoughts),
                "actions": list(branch_actions),
                "post_img": post_name_unique,
                "accepted": decision.accept,
                "rollback_to": decision.rollback_to if not decision.accept else None,
                "reason": decision.reason,
                "correction": None,         # filled in after second-shot
                "correction_raw": "",
            }

            # ----- 3. Apply decision -----
            # Only accept the branch (and any terminate inside it) when the
            # teacher explicitly approves. Don't auto-accept on terminate.
            if decision.accept:
                if branch_done:
                    is_done = True
                    final_result = pending_done_text
                self._branch_records.append(branch_record)
                self._teacher_decisions.append({
                    **decision.to_record(),
                    "branch_start": branch_start,
                    "branch_len": len(branch),
                    "branch_no": branch_no,
                })
                if is_done:
                    break
                continue

            if self._teacher_interventions >= self.max_interventions:
                reason = "max teacher interventions reached; discarding trajectory"
                errors.append(reason)
                branch_record["accepted"] = False
                branch_record["discarded"] = True
                branch_record["discard_reason"] = reason
                is_done = False
                final_result = None
                self._branch_records.append(branch_record)
                self._teacher_decisions.append({
                    **decision.to_record(),
                    "branch_start": branch_start,
                    "branch_len": len(branch),
                    "branch_no": branch_no,
                    "discarded": True,
                    "discard_reason": reason,
                })
                break

            rb = max(0, min(decision.rollback_to, len(branch) - 1))
            keep_in_branch = rb  # number of student steps in branch we keep
            new_total = branch_start + keep_in_branch  # absolute step count after rollback

            # Bail out of repeated-target loops: if the teacher has rolled
            # back to this same absolute step >=2 times already, accept the
            # current branch instead — the correction is clearly ineffective.
            self._rollback_target_hits[new_total] = (
                self._rollback_target_hits.get(new_total, 0) + 1)
            if self._rollback_target_hits[new_total] > 2:
                reason = (
                    f"abandoning rollback: target step {new_total} hit "
                    f"{self._rollback_target_hits[new_total]} times; "
                    "discarding trajectory"
                )
                errors.append(reason)
                branch_record["reason"] = (
                    branch_record.get("reason", "")
                    + f" [DISCARDED - target {new_total} repeated]")
                branch_record["accepted"] = False
                branch_record["discarded"] = True
                branch_record["discard_reason"] = reason
                is_done = False
                final_result = None
                self._branch_records.append(branch_record)
                self._teacher_decisions.append({
                    **decision.to_record(),
                    "branch_start": branch_start,
                    "branch_len": len(branch),
                    "branch_no": branch_no,
                    "discarded": True,
                    "discard_reason": reason,
                })
                break

            # Roll the env back via reset+replay.
            await self._rollback_to(new_total)
            self._truncate_state(new_total)
            # Truncate the canonical history too so report.py's step_{i}.png
            # indexing stays consistent. Anything that happened past
            # branch_start + keep_in_branch in this branch is discarded.
            del history[branch_history_start + keep_in_branch:]

            # Rollback verification: re-take a screenshot RIGHT after the
            # rollback completes, so a human can compare it to the screen
            # the student saw before the (now-discarded) action at this step.
            try:
                verify_ss = await self.take_screenshot()
                verify_name = f"b{branch_no}_rb_to_{new_total}.png"
                (screenshots_dir / verify_name).write_bytes(verify_ss)
                branch_record["rb_verify_img"] = verify_name
                tracer = getattr(self, "_tracer", None)
                if tracer is not None:
                    tracer.register(verify_ss, screenshots_dir / verify_name)
                if 0 <= keep_in_branch < len(branch_step_imgs):
                    branch_record["rb_expected_img"] = branch_step_imgs[keep_in_branch]
                elif branch_start > 0 and self._branch_records:
                    branch_record["rb_expected_img"] = self._branch_records[-1].get("post_img")
            except Exception as e:
                errors.append(f"rb verify error: {e}")

            # ---- SECOND-SHOT teacher review ---------------------------
            # The first shot only decided accept/rollback_to.  We now ask
            # the teacher again with the *student's own Qwen prompt format*
            # (same system prompt, same XML <tool_call> output schema), so
            # the teacher behaves like a stronger version of the student.
            # The correction prompt uses a configurable recent-image window
            # plus the rollback reason.
            corrections: list[dict] = []
            actions: list[dict] = []
            corr_xml = ""
            try:
                rb_ss = await self.take_screenshot()
                rb_name = f"b{branch_no}_rb_corr_input.png"
                (screenshots_dir / rb_name).write_bytes(rb_ss)
                tracer = getattr(self, "_tracer", None)
                if tracer is not None:
                    tracer.register(rb_ss, screenshots_dir / rb_name)
                rb_b64 = base64.b64encode(rb_ss).decode()
                msgs = self._build_qwen_correction_messages(
                    task=task,
                    server_url=server_url,
                    current_screenshot_b64=rb_b64,
                    rollback_reason=decision.reason,
                    image_max=getattr(self.teacher, "correction_image_max", 6),
                )
                corr_xml = await self.teacher.review_correction(messages=msgs)
                # Parse EVERY <tool_call>...</tool_call> block. Some
                # teacher outputs chain calls (e.g. mouse_move + scroll);
                # picking only the first silently drops actions.
                for tc in re.finditer(r"<tool_call>(.*?)</tool_call>",
                                      corr_xml, re.DOTALL):
                    params = self._parse_xml_tool_call(tc.group(1))
                    if not params:
                        continue
                    corrections.append(params)
                    actions.extend(self._tool_params_to_actions(params))
            except Exception as e:
                errors.append(f"second-shot teacher error: {e}")
            decision.correction = corrections or None
            branch_record["correction"] = corrections or None
            branch_record["correction_raw"] = corr_xml[:2000]

            # Apply teacher correction as one synthetic step
            if actions:
                # Take the screenshot the corrective action will see
                corr_ss = await self.take_screenshot()
                # Write under both the canonical step name (so report.py
                # can find it) AND a per-branch name (so viz can show
                # rollback history without clobbering).
                (screenshots_dir / f"step_{new_total}.png").write_bytes(corr_ss)
                corr_name = f"corr_{new_total}.png"
                (screenshots_dir / corr_name).write_bytes(corr_ss)
                corr_name_unique = f"b{branch_no}_corr.png"
                (screenshots_dir / corr_name_unique).write_bytes(corr_ss)
                branch_record["corr_img"] = corr_name_unique
                tracer = getattr(self, "_tracer", None)
                if tracer is not None:
                    tracer.register(corr_ss,
                                    screenshots_dir / f"step_{new_total}.png")
                b64 = base64.b64encode(corr_ss).decode()
                self._screenshots_b64.append(b64)
                # Use the teacher's actual XML output verbatim so the
                # student's running history sees a syntactically real
                # Qwen response (not a reconstructed one).
                first_corr = corrections[0] if corrections else {}
                self._responses.append(
                    corr_xml or _correction_to_xml(first_corr)[0]
                )
                self._action_summaries.append(
                    "teacher: " + ", ".join(
                        c.get("action", "unknown") for c in corrections
                    )
                )
                self._executed_per_step.append(list(actions))

                history.append({
                    "step": new_total,
                    "phase": "teacher_correction",
                    "branch_no": branch_no,
                    "correction": corrections,
                    "actions": actions,
                    "reason": decision.reason,
                })

                done, done_text = await self._execute_teacher_actions(
                    actions,
                    errors=errors,
                    server_url=server_url,
                )
                if done:
                    is_done = True
                    final_result = done_text

                step = new_total + 1
                self._teacher_interventions += 1
                self._branch_records.append(branch_record)
                self._teacher_decisions.append({
                    **decision.to_record(),
                    "branch_start": branch_start,
                    "branch_len": len(branch),
                    "branch_no": branch_no,
                })
                if is_done:
                    break
                continue

            # No usable correction — just keep the rollback prefix and continue
            step = new_total
            self._teacher_interventions += 1
            self._branch_records.append(branch_record)
            self._teacher_decisions.append({
                **decision.to_record(),
                "branch_start": branch_start,
                "branch_len": len(branch),
                "branch_no": branch_no,
                "no_correction": True,
            })

        return {
            "steps": len(self._executed_per_step),
            "is_done": is_done,
            "final_result": final_result,
            "errors": errors,
            "history": history,
        }

    # ------------------------------------------------------------------ wrappers

    async def _call_with_retry(self):
        """Re-uses the base helper but exposes a stable name."""
        from vision_agents import _async_retry_step_api_call
        return await _async_retry_step_api_call(lambda: self._call_llm_inner())

    # ------------------------------------------------------------------ post-task

    async def run(self, task: str, server_url: str, task_dir: Path) -> AgentResult:
        result = await super().run(task, server_url, task_dir)
        # Persist teacher decisions + branch metadata next to history.json.
        try:
            (task_dir / "rollout_meta.json").write_text(json.dumps({
                "K": self.K,
                "teacher_interventions": self._teacher_interventions,
                "teacher_decisions": self._teacher_decisions,
                "actions_per_step": self._executed_per_step,
                "branches": getattr(self, "_branch_records", []),
            }, indent=2))
        except Exception as e:
            result.errors.append(f"meta save error: {e}")
        # Stash payload for QD archive admission (verifier verdict not known
        # at this layer — runner will admit after verification).
        self._last_traj_payload = {
            "actions_per_step": list(self._executed_per_step),
            "teacher_interventions": self._teacher_interventions,
            "teacher_decisions": list(self._teacher_decisions),
            "task_dir": str(task_dir),
        }
        return result

    def admit_to_archive(self, *, task_id: str, passed: bool) -> dict | None:
        if self.archive is None or not hasattr(self, "_last_traj_payload"):
            return None
        return self.archive.admit(
            task_id=task_id,
            passed=passed,
            trajectory=self._last_traj_payload,
        )


class BranchingRolloutAgent(RolloutAgent):
    """Forked SRC rollout.

    On teacher rejection, keep the rejected student branch as one logical
    child leaf and continue the corrected teacher branch in the current leaf.
    Leaves are executed sequentially by reset+replay in one browser session;
    each terminal leaf is verified and admitted to the QD archive separately.
    """

    def __init__(
        self,
        *,
        max_forks: int = 4,
        max_leaves: int = 8,
        branch_workers: int = 2,
        branch_base_port: int | None = None,
        env_host: str = "localhost",
        **kw,
    ):
        super().__init__(**kw)
        self.max_forks = max(0, max_forks)
        self.max_leaves = max(1, max_leaves)
        self.branch_workers = max(1, branch_workers)
        self.branch_base_port = branch_base_port
        self.env_host = env_host
        self._coordinator = _ForkCoordinator(
            max_forks=self.max_forks,
            max_leaves=self.max_leaves,
        )

    # ------------------------------------------------------------- leaf state

    def _coord(self) -> _ForkCoordinator:
        return self._coordinator

    def _next_leaf_id(self) -> str:
        coord = self._coord()
        leaf_id = f"leaf_{coord.leaf_counter:03d}"
        coord.leaf_counter += 1
        return leaf_id

    def _next_branch_no(self) -> int:
        coord = self._coord()
        coord.global_branch_no += 1
        return coord.global_branch_no

    def _new_leaf(
        self,
        *,
        parent_id: str | None = None,
        role: str = "root",
        fork_reason: str = "",
    ) -> _ForkLeafState:
        return _ForkLeafState(
            leaf_id=self._next_leaf_id(),
            parent_id=parent_id,
            role=role,
            fork_reason=fork_reason,
        )

    def _load_leaf_state(self, leaf: _ForkLeafState) -> None:
        self._screenshots_b64 = copy.deepcopy(leaf.screenshots_b64)
        self._responses = copy.deepcopy(leaf.responses)
        self._action_summaries = copy.deepcopy(leaf.action_summaries)
        self._folded_prefix_k = min(
            leaf.folded_prefix_k, len(self._screenshots_b64)
        )
        self._executed_per_step = copy.deepcopy(leaf.executed_per_step)
        self._teacher_decisions = copy.deepcopy(leaf.teacher_decisions)
        self._teacher_interventions = leaf.teacher_interventions
        self._rollback_target_hits = copy.deepcopy(leaf.rollback_target_hits)
        self._branch_records = copy.deepcopy(leaf.branch_records)
        self._live_history = copy.deepcopy(leaf.history)
        self._live_errors = copy.deepcopy(leaf.errors)

    def _capture_leaf_state(
        self,
        leaf: _ForkLeafState,
        *,
        is_done: bool | None = None,
        final_result: str | None = None,
        discarded: bool | None = None,
        discard_reason: str | None = None,
    ) -> _ForkLeafState:
        leaf.screenshots_b64 = copy.deepcopy(self._screenshots_b64)
        leaf.responses = copy.deepcopy(self._responses)
        leaf.action_summaries = copy.deepcopy(self._action_summaries)
        leaf.folded_prefix_k = int(getattr(self, "_folded_prefix_k", 0))
        leaf.executed_per_step = copy.deepcopy(self._executed_per_step)
        leaf.teacher_decisions = copy.deepcopy(self._teacher_decisions)
        leaf.teacher_interventions = int(self._teacher_interventions)
        leaf.rollback_target_hits = copy.deepcopy(self._rollback_target_hits)
        leaf.branch_records = copy.deepcopy(self._branch_records)
        leaf.history = copy.deepcopy(self._live_history)
        leaf.errors = copy.deepcopy(self._live_errors)
        if is_done is not None:
            leaf.is_done = is_done
        if final_result is not None:
            leaf.final_result = final_result
        if discarded is not None:
            leaf.discarded = discarded
        if discard_reason is not None:
            leaf.discard_reason = discard_reason
        return leaf

    def _can_fork(self) -> bool:
        coord = self._coord()
        return coord.forks_used < coord.max_forks and coord.leaf_counter < coord.max_leaves

    def _note_fork(self) -> None:
        self._coord().forks_used += 1

    @staticmethod
    async def _enqueue_leaf(
        pending: list[_ForkLeafState] | asyncio.Queue,
        leaf: _ForkLeafState,
    ) -> None:
        if isinstance(pending, asyncio.Queue):
            await pending.put(leaf)
        else:
            pending.append(leaf)

    def _leaf_payload(self, leaf: _ForkLeafState, task_dir: Path) -> dict:
        return {
            "actions_per_step": copy.deepcopy(leaf.executed_per_step),
            "teacher_interventions": leaf.teacher_interventions,
            "teacher_decisions": copy.deepcopy(leaf.teacher_decisions),
            "task_dir": str(task_dir / "leaves" / leaf.leaf_id),
            "branching": True,
            "leaf_id": leaf.leaf_id,
            "parent_id": leaf.parent_id,
            "role": leaf.role,
            "fork_reason": leaf.fork_reason,
            "discarded": leaf.discarded,
            "discard_reason": leaf.discard_reason,
        }

    # --------------------------------------------------------------- execution

    async def _run_leaf_to_terminal(
        self,
        leaf: _ForkLeafState,
        *,
        task: str,
        server_url: str,
        screenshots_dir: Path,
        pending: list[_ForkLeafState] | asyncio.Queue,
        terminals: list[_ForkLeafState],
        verify_fn: Callable[[str], tuple[bool, str]] | None = None,
    ) -> None:
        """Continue one logical leaf until done, budgeted out, or max steps."""
        leaf_ss_dir = screenshots_dir / leaf.leaf_id
        leaf_ss_dir.mkdir(parents=True, exist_ok=True)

        self._task = task
        self._server_url_task = server_url
        await self._reset_env_and_replay(leaf.executed_per_step)
        self._load_leaf_state(leaf)

        consecutive_failures = 0
        empty_output_count = 0
        final_result: str | None = leaf.final_result
        is_done = leaf.is_done

        while len(self._executed_per_step) < self.max_steps and not is_done:
            if consecutive_failures >= self.max_consecutive_failures:
                self._live_errors.append(
                    f"Stopping after {consecutive_failures} consecutive failures"
                )
                break

            branch_start = len(self._executed_per_step)
            branch_history_start = len(self._live_history)
            branch_no = self._next_branch_no()
            branch: list[BranchStep] = []
            branch_done = False
            pending_done_text: str | None = None
            empty_takeover = False
            empty_takeover_reason = ""
            empty_takeover_screenshot: bytes | None = None
            empty_takeover_step = branch_start
            branch_step_imgs: list[str] = []
            branch_thoughts: list[str] = []
            branch_actions: list[list[dict]] = []

            for _ in range(self.K):
                step = len(self._executed_per_step)
                if step >= self.max_steps:
                    break
                if not await self._check_browser_health():
                    self._live_errors.append(f"Browser unrecoverable at step {step}")
                    is_done = True
                    break

                screenshot = await self.take_screenshot()
                ss_path = leaf_ss_dir / f"step_{step}.png"
                ss_path.write_bytes(screenshot)
                bs_name = f"b{branch_no}_s{len(branch)}.png"
                (leaf_ss_dir / bs_name).write_bytes(screenshot)
                branch_step_imgs.append(f"{leaf.leaf_id}/{bs_name}")

                tracer = getattr(self, "_tracer", None)
                if tracer is not None:
                    tracer.register(screenshot, ss_path)

                self._prepare_step(step, screenshot)
                response, api_err = await self._call_with_retry()
                if api_err:
                    self._live_errors.append(f"Student API error at step {step}: {api_err}")
                    consecutive_failures += 1
                    break

                result = self._parse_response(response)
                if (
                    not result.actions
                    and not result.is_done
                    and not result.action_descriptions
                ):
                    empty_output_count += 1
                    consecutive_failures += 1
                    if len(self._screenshots_b64) > len(self._executed_per_step):
                        self._screenshots_b64.pop()
                    if len(self._responses) > len(self._executed_per_step):
                        self._responses.pop()
                    if len(self._action_summaries) > len(self._executed_per_step):
                        self._action_summaries.pop()
                    if empty_output_count >= 3:
                        empty_takeover = True
                        empty_takeover_reason = (
                            "student produced 3 consecutive empty outputs; "
                            "teacher taking over current state"
                        )
                        empty_takeover_screenshot = screenshot
                        empty_takeover_step = step
                        self._live_errors.append(empty_takeover_reason)
                        break
                    continue

                consecutive_failures = 0
                empty_output_count = 0

                actions_this_step = list(result.actions)
                self._executed_per_step.append(actions_this_step)
                branch_thoughts.append((result.text or "")[:2000])
                branch_actions.append(actions_this_step)

                self._live_history.append({
                    "step": step,
                    "phase": "student_branch",
                    "leaf_id": leaf.leaf_id,
                    "branch_start": branch_start,
                    "branch_no": branch_no,
                    "thought": result.text,
                    "actions": actions_this_step,
                })

                branch.append(BranchStep(
                    index_in_branch=len(branch),
                    screenshot_b64=base64.b64encode(screenshot).decode(),
                    thought=result.text or "",
                    action_summary=(
                        self._action_summaries[-1]
                        if self._action_summaries else ""
                    ),
                    action_dicts=actions_this_step,
                ))

                if result.is_done:
                    branch_done = True
                    pending_done_text = result.text
                    break

                await self._execute_step(step, result)
                self._on_step_done(step, result, screenshot)

            if empty_takeover:
                step = len(self._executed_per_step)
                screenshot_for_teacher = (
                    empty_takeover_screenshot
                    if empty_takeover_screenshot is not None
                    else await self.take_screenshot()
                )
                empty_name = f"b{branch_no}_empty_takeover.png"
                (leaf_ss_dir / empty_name).write_bytes(screenshot_for_teacher)
                tracer = getattr(self, "_tracer", None)
                if tracer is not None:
                    tracer.register(screenshot_for_teacher, leaf_ss_dir / empty_name)
                b64 = base64.b64encode(screenshot_for_teacher).decode()

                if self._teacher_interventions >= self.max_interventions:
                    reason = (
                        "max teacher interventions reached during "
                        "empty-output fallback; discarding leaf"
                    )
                    self._live_errors.append(reason)
                    branch_record = {
                        "leaf_id": leaf.leaf_id,
                        "branch_no": branch_no,
                        "branch_start": branch_start,
                        "branch_len": len(branch),
                        "step_imgs": list(branch_step_imgs),
                        "thoughts": list(branch_thoughts),
                        "actions": list(branch_actions),
                        "post_img": f"{leaf.leaf_id}/{empty_name}",
                        "accepted": False,
                        "rollback_to": step,
                        "reason": empty_takeover_reason,
                        "empty_output_fallback": True,
                        "empty_output_step": empty_takeover_step,
                        "discarded": True,
                        "discard_reason": reason,
                        "correction": None,
                        "correction_raw": "",
                    }
                    leaf.discarded = True
                    leaf.discard_reason = reason
                    is_done = False
                    final_result = None
                    self._branch_records.append(branch_record)
                    self._teacher_decisions.append({
                        "accept": False,
                        "rollback_to": step,
                        "reason": empty_takeover_reason,
                        "raw": "",
                        "branch_start": branch_start,
                        "branch_len": len(branch),
                        "branch_no": branch_no,
                        "leaf_id": leaf.leaf_id,
                        "empty_output_fallback": True,
                        "discarded": True,
                        "discard_reason": reason,
                    })
                    break

                corrections: list[dict] = []
                actions: list[dict] = []
                corr_xml = ""
                try:
                    corrections, actions, corr_xml = (
                        await self._request_teacher_correction(
                            task=task,
                            server_url=server_url,
                            current_screenshot_b64=b64,
                            rollback_reason=empty_takeover_reason,
                        )
                    )
                except Exception as e:
                    self._live_errors.append(f"empty-output teacher error: {e}")

                branch_record = {
                    "leaf_id": leaf.leaf_id,
                    "branch_no": branch_no,
                    "branch_start": branch_start,
                    "branch_len": len(branch),
                    "step_imgs": list(branch_step_imgs),
                    "thoughts": list(branch_thoughts),
                    "actions": list(branch_actions),
                    "post_img": f"{leaf.leaf_id}/{empty_name}",
                    "accepted": False,
                    "rollback_to": step,
                    "reason": empty_takeover_reason,
                    "empty_output_fallback": True,
                    "empty_output_step": empty_takeover_step,
                    "correction": corrections or None,
                    "correction_raw": corr_xml[:2000],
                }

                if actions:
                    (leaf_ss_dir / f"step_{step}.png").write_bytes(
                        screenshot_for_teacher
                    )
                    corr_name_unique = f"b{branch_no}_empty_corr.png"
                    (leaf_ss_dir / corr_name_unique).write_bytes(
                        screenshot_for_teacher
                    )
                    branch_record["corr_img"] = f"{leaf.leaf_id}/{corr_name_unique}"
                    if tracer is not None:
                        tracer.register(
                            screenshot_for_teacher,
                            leaf_ss_dir / f"step_{step}.png",
                        )

                    self._screenshots_b64.append(b64)
                    first_corr = corrections[0] if corrections else {}
                    self._responses.append(
                        corr_xml or _correction_to_xml(first_corr)[0]
                    )
                    self._action_summaries.append(
                        "teacher: " + ", ".join(
                            c.get("action", "unknown") for c in corrections
                        )
                    )
                    self._executed_per_step.append(list(actions))
                    self._live_history.append({
                        "step": step,
                        "phase": "teacher_correction",
                        "leaf_id": leaf.leaf_id,
                        "branch_no": branch_no,
                        "correction": corrections,
                        "actions": actions,
                        "reason": empty_takeover_reason,
                        "empty_output_fallback": True,
                    })

                    done, done_text = await self._execute_teacher_actions(
                        actions,
                        errors=self._live_errors,
                        server_url=server_url,
                        verify_fn=verify_fn,
                        verifier_target=branch_record,
                    )
                    if done:
                        is_done = True
                        final_result = done_text

                    self._teacher_interventions += 1
                    self._branch_records.append(branch_record)
                    self._teacher_decisions.append({
                        "accept": False,
                        "rollback_to": step,
                        "reason": empty_takeover_reason,
                        "raw": corr_xml[:2000],
                        "branch_start": branch_start,
                        "branch_len": len(branch),
                        "branch_no": branch_no,
                        "leaf_id": leaf.leaf_id,
                        "empty_output_fallback": True,
                        "correction": corrections or None,
                    })
                    consecutive_failures = 0
                    empty_output_count = 0
                    continue

                reason = (
                    "empty-output fallback teacher returned no executable "
                    "correction; discarding leaf"
                )
                self._live_errors.append(reason)
                branch_record["discarded"] = True
                branch_record["discard_reason"] = reason
                leaf.discarded = True
                leaf.discard_reason = reason
                is_done = False
                final_result = None
                self._teacher_interventions += 1
                self._branch_records.append(branch_record)
                self._teacher_decisions.append({
                    "accept": False,
                    "rollback_to": step,
                    "reason": empty_takeover_reason,
                    "raw": corr_xml[:2000],
                    "branch_start": branch_start,
                    "branch_len": len(branch),
                    "branch_no": branch_no,
                    "leaf_id": leaf.leaf_id,
                    "empty_output_fallback": True,
                    "discarded": True,
                    "discard_reason": reason,
                    "correction": corrections or None,
                })
                break

            if not branch:
                if is_done:
                    break
                continue

            post_branch_ss = await self.take_screenshot()
            post_name_unique = f"b{branch_no}_post.png"
            (leaf_ss_dir / post_name_unique).write_bytes(post_branch_ss)
            post_rel = f"{leaf.leaf_id}/{post_name_unique}"
            tracer = getattr(self, "_tracer", None)
            if tracer is not None:
                tracer.register(post_branch_ss, leaf_ss_dir / post_name_unique)

            verifier_feedback = None
            if branch_done and verify_fn is not None:
                try:
                    v_passed, v_msg = await asyncio.to_thread(
                        verify_fn, server_url
                    )
                except Exception as e:
                    v_passed, v_msg = False, f"Verifier exception: {e}"
                verifier_feedback = {"passed": v_passed, "message": v_msg}

            decision: TeacherDecision = await self.teacher.review(
                task=task,
                server_url=server_url,
                branch_start=branch_start,
                branch=branch,
                post_branch_screenshot_b64=base64.b64encode(post_branch_ss).decode(),
                accepted_prefix=self._teacher_review_context(branch_start),
                verifier_feedback=verifier_feedback,
            )

            branch_record = {
                "leaf_id": leaf.leaf_id,
                "branch_no": branch_no,
                "branch_start": branch_start,
                "branch_len": len(branch),
                "step_imgs": list(branch_step_imgs),
                "thoughts": list(branch_thoughts),
                "actions": list(branch_actions),
                "post_img": post_rel,
                "accepted": decision.accept,
                "rollback_to": decision.rollback_to if not decision.accept else None,
                "reason": decision.reason,
                "correction": None,
                "correction_raw": "",
            }

            if (
                branch_done
                and decision.accept
                and verifier_feedback is not None
                and not verifier_feedback.get("passed")
            ):
                msg = str(verifier_feedback.get("message", ""))
                decision = TeacherDecision(
                    accept=False,
                    rollback_to=max(0, len(branch) - 1),
                    reason=f"Terminate rejected by hard verifier: {msg}"[:400],
                    raw=decision.raw,
                    error=decision.error,
                )
                branch_record["accepted"] = False
                branch_record["rollback_to"] = decision.rollback_to
                branch_record["reason"] = decision.reason
                branch_record["terminate_verifier"] = verifier_feedback
                branch_record["skip_student_fork"] = True
            elif verifier_feedback is not None:
                branch_record["terminate_verifier"] = verifier_feedback

            if decision.accept:
                if branch_done:
                    is_done = True
                    final_result = pending_done_text
                self._branch_records.append(branch_record)
                self._teacher_decisions.append({
                    **decision.to_record(),
                    "branch_start": branch_start,
                    "branch_len": len(branch),
                    "branch_no": branch_no,
                    "leaf_id": leaf.leaf_id,
                })
                continue

            if self._teacher_interventions >= self.max_interventions:
                reason = "max teacher interventions reached; discarding leaf"
                self._live_errors.append(reason)
                branch_record["accepted"] = False
                branch_record["discarded"] = True
                branch_record["discard_reason"] = reason
                leaf.discarded = True
                leaf.discard_reason = reason
                is_done = False
                final_result = None
                self._branch_records.append(branch_record)
                self._teacher_decisions.append({
                    **decision.to_record(),
                    "branch_start": branch_start,
                    "branch_len": len(branch),
                    "branch_no": branch_no,
                    "leaf_id": leaf.leaf_id,
                    "discarded": True,
                    "discard_reason": reason,
                })
                break

            rb = max(0, min(decision.rollback_to, len(branch) - 1))
            keep_in_branch = rb
            new_total = branch_start + keep_in_branch

            self._rollback_target_hits[new_total] = (
                self._rollback_target_hits.get(new_total, 0) + 1
            )
            if self._rollback_target_hits[new_total] > 2:
                reason = (
                    f"discarding leaf: rollback target step {new_total} hit "
                    f"{self._rollback_target_hits[new_total]} times"
                )
                self._live_errors.append(reason)
                branch_record["accepted"] = False
                branch_record["discarded"] = True
                branch_record["discard_reason"] = reason
                branch_record["reason"] = (
                    branch_record.get("reason", "")
                    + f" [DISCARDED - target {new_total} repeated]"
                )
                leaf.discarded = True
                leaf.discard_reason = reason
                is_done = False
                final_result = None
                self._branch_records.append(branch_record)
                self._teacher_decisions.append({
                    **decision.to_record(),
                    "branch_start": branch_start,
                    "branch_len": len(branch),
                    "branch_no": branch_no,
                    "leaf_id": leaf.leaf_id,
                    "discarded": True,
                    "discard_reason": reason,
                })
                break

            if self._can_fork() and not branch_record.get("skip_student_fork"):
                student_child = self._new_leaf(
                    parent_id=leaf.leaf_id,
                    role="student_rejected_branch",
                    fork_reason=decision.reason,
                )
                self._capture_leaf_state(
                    student_child,
                    is_done=branch_done,
                    final_result=pending_done_text if branch_done else None,
                )
                student_record = {
                    **decision.to_record(),
                    "branch_start": branch_start,
                    "branch_len": len(branch),
                    "branch_no": branch_no,
                    "leaf_id": student_child.leaf_id,
                    "parent_leaf_id": leaf.leaf_id,
                    "kept_for_exploration": True,
                }
                student_branch_record = copy.deepcopy(branch_record)
                student_branch_record["leaf_id"] = student_child.leaf_id
                student_branch_record["kept_for_exploration"] = True
                student_child.teacher_decisions.append(student_record)
                student_child.branch_records.append(student_branch_record)
                self._note_fork()
                if student_child.is_done or student_child.steps >= self.max_steps:
                    terminals.append(student_child)
                else:
                    await self._enqueue_leaf(pending, student_child)

            await self._rollback_to(new_total)
            self._truncate_state(new_total)
            del self._live_history[branch_history_start + keep_in_branch:]

            try:
                verify_ss = await self.take_screenshot()
                verify_name = f"b{branch_no}_rb_to_{new_total}.png"
                (leaf_ss_dir / verify_name).write_bytes(verify_ss)
                branch_record["rb_verify_img"] = f"{leaf.leaf_id}/{verify_name}"
                tracer = getattr(self, "_tracer", None)
                if tracer is not None:
                    tracer.register(verify_ss, leaf_ss_dir / verify_name)
                if 0 <= keep_in_branch < len(branch_step_imgs):
                    branch_record["rb_expected_img"] = branch_step_imgs[keep_in_branch]
                elif branch_start > 0 and self._branch_records:
                    branch_record["rb_expected_img"] = self._branch_records[-1].get("post_img")
            except Exception as e:
                self._live_errors.append(f"rb verify error: {e}")

            corrections: list[dict] = []
            actions: list[dict] = []
            corr_xml = ""
            try:
                rb_ss = await self.take_screenshot()
                rb_name = f"b{branch_no}_rb_corr_input.png"
                (leaf_ss_dir / rb_name).write_bytes(rb_ss)
                tracer = getattr(self, "_tracer", None)
                if tracer is not None:
                    tracer.register(rb_ss, leaf_ss_dir / rb_name)
                msgs = self._build_qwen_correction_messages(
                    task=task,
                    server_url=server_url,
                    current_screenshot_b64=base64.b64encode(rb_ss).decode(),
                    rollback_reason=decision.reason,
                    image_max=getattr(self.teacher, "correction_image_max", 6),
                )
                corr_xml = await self.teacher.review_correction(messages=msgs)
                for tc in re.finditer(r"<tool_call>(.*?)</tool_call>", corr_xml, re.DOTALL):
                    params = self._parse_xml_tool_call(tc.group(1))
                    if not params:
                        continue
                    corrections.append(params)
                    actions.extend(self._tool_params_to_actions(params))
            except Exception as e:
                self._live_errors.append(f"second-shot teacher error: {e}")

            decision.correction = corrections or None
            branch_record["correction"] = corrections or None
            branch_record["correction_raw"] = corr_xml[:2000]

            if actions:
                corr_ss = await self.take_screenshot()
                (leaf_ss_dir / f"step_{new_total}.png").write_bytes(corr_ss)
                corr_name_unique = f"b{branch_no}_corr.png"
                (leaf_ss_dir / corr_name_unique).write_bytes(corr_ss)
                branch_record["corr_img"] = f"{leaf.leaf_id}/{corr_name_unique}"
                tracer = getattr(self, "_tracer", None)
                if tracer is not None:
                    tracer.register(corr_ss, leaf_ss_dir / f"step_{new_total}.png")

                self._screenshots_b64.append(base64.b64encode(corr_ss).decode())
                first_corr = corrections[0] if corrections else {}
                self._responses.append(
                    corr_xml or _correction_to_xml(first_corr)[0]
                )
                self._action_summaries.append(
                    "teacher: " + ", ".join(
                        c.get("action", "unknown") for c in corrections
                    )
                )
                self._executed_per_step.append(list(actions))

                self._live_history.append({
                    "step": new_total,
                    "phase": "teacher_correction",
                    "leaf_id": leaf.leaf_id,
                    "branch_no": branch_no,
                    "correction": corrections,
                    "actions": actions,
                    "reason": decision.reason,
                })

                done, done_text = await self._execute_teacher_actions(
                    actions,
                    errors=self._live_errors,
                    server_url=server_url,
                    verify_fn=verify_fn,
                    verifier_target=branch_record,
                )
                if done:
                    is_done = True
                    final_result = done_text

                self._teacher_interventions += 1
                self._branch_records.append(branch_record)
                self._teacher_decisions.append({
                    **decision.to_record(),
                    "branch_start": branch_start,
                    "branch_len": len(branch),
                    "branch_no": branch_no,
                    "leaf_id": leaf.leaf_id,
                })
                continue

            self._teacher_interventions += 1
            self._branch_records.append(branch_record)
            self._teacher_decisions.append({
                **decision.to_record(),
                "branch_start": branch_start,
                "branch_len": len(branch),
                "branch_no": branch_no,
                "leaf_id": leaf.leaf_id,
                "no_correction": True,
            })

        self._capture_leaf_state(
            leaf,
            is_done=is_done,
            final_result=final_result,
        )
        terminals.append(leaf)

    async def _verify_leaf(
        self,
        leaf: _ForkLeafState,
        *,
        server_url: str,
        verify_fn: Callable[[str], tuple[bool, str]],
    ) -> tuple[bool, str]:
        await self._reset_env_and_replay(leaf.executed_per_step)
        try:
            return verify_fn(server_url)
        except Exception as e:
            return False, f"Verifier exception: {e}"

    def _make_parallel_worker_agent(self) -> "BranchingRolloutAgent":
        teacher = TeacherReviewer(
            base_url=getattr(self.teacher, "base_url", None),
            api_key=getattr(self.teacher, "api_key", None),
            model=getattr(self.teacher, "model", None),
            max_tokens=getattr(self.teacher, "max_tokens", 19200),
            temperature=getattr(self.teacher, "temperature", 0.0),
            review_context_steps=getattr(self.teacher, "review_context_steps", 4),
            correction_image_max=getattr(self.teacher, "correction_image_max", 6),
        )
        worker = BranchingRolloutAgent(
            max_steps=self.max_steps,
            timeout=self.timeout,
            headless=self.headless,
            K=self.K,
            teacher=teacher,
            archive=self.archive,
            max_interventions=self.max_interventions,
            max_forks=self.max_forks,
            max_leaves=self.max_leaves,
            branch_workers=1,
            branch_base_port=None,
            env_host=self.env_host,
            model=getattr(self, "MODEL", None),
            image_max=getattr(self, "_image_max", 1),
            fold_size=getattr(self, "_fold_size", 100),
            history_n=getattr(self, "_history_n", 100),
        )
        worker._coordinator = self._coordinator
        return worker

    async def run_with_verifier(
        self,
        *,
        task: dict,
        server_url: str,
        web_app_dir: str,
        task_dir: Path,
        verify_fn: Callable[[str], tuple[bool, str]],
    ) -> dict:
        """Run forked rollout and verify/admit every terminal leaf."""
        task_dir.mkdir(parents=True, exist_ok=True)
        screenshots_dir = task_dir / "screenshots"
        screenshots_dir.mkdir(exist_ok=True)
        leaves_dir = task_dir / "leaves"
        leaves_dir.mkdir(exist_ok=True)

        self._tracer = LLMTracer(task_dir)
        self._live_history = []
        self._live_errors = []
        self._coordinator = _ForkCoordinator(
            max_forks=self.max_forks,
            max_leaves=self.max_leaves,
        )
        self._init_conversation(task["instruction"], server_url)
        if self.teacher is not None:
            self.teacher.tracer = self._tracer

        t0 = time.time()
        root_leaf = self._new_leaf(role="root")
        terminals: list[_ForkLeafState] = []
        rollout_errors: list[str] = []
        worker_specs: list[tuple[BranchingRolloutAgent, str, object | None]] = [
            (self, server_url, None)
        ]
        leaf_worker_tasks: list[asyncio.Task] = []
        verify_worker_tasks: list[asyncio.Task] = []

        parallel_ok = (
            self.branch_workers > 1
            and self.env_host in ("localhost", "127.0.0.1")
            and self.branch_base_port is not None
        )
        if self.branch_workers > 1 and not parallel_ok:
            rollout_errors.append(
                "parallel branching requested but no local branch_base_port "
                "is available; falling back to sequential leaf scheduling"
            )

        if parallel_ok:
            from server import start_server, stop_server, wait_for_server

            for i in range(1, self.branch_workers):
                port = self.branch_base_port + i - 1
                proc = start_server(web_app_dir, port)
                if not wait_for_server(port, host=self.env_host):
                    stop_server(proc)
                    rollout_errors.append(
                        f"branch worker server failed on port {port}"
                    )
                    continue
                url = f"http://{self.env_host}:{port}"
                worker = self._make_parallel_worker_agent()
                worker._tracer = self._tracer
                worker.teacher.tracer = self._tracer
                try:
                    await asyncio.wait_for(
                        worker.setup(url),
                        timeout=BRANCH_AGENT_SETUP_TIMEOUT,
                    )
                except Exception as e:
                    try:
                        await asyncio.wait_for(
                            worker.teardown(),
                            timeout=BRANCH_AGENT_TEARDOWN_TIMEOUT,
                        )
                    except Exception:
                        pass
                    stop_server(proc)
                    rollout_errors.append(
                        f"branch worker setup failed on port {port}: {e}"
                    )
                    continue
                worker_specs.append((worker, url, proc))

        try:
            if len(worker_specs) <= 1:
                pending: list[_ForkLeafState] = [root_leaf]
                while pending:
                    leaf = pending.pop(0)
                    await self._run_leaf_to_terminal(
                        leaf,
                        task=task["instruction"],
                        server_url=server_url,
                        screenshots_dir=screenshots_dir,
                        pending=pending,
                        terminals=terminals,
                        verify_fn=verify_fn,
                    )
            else:
                pending_q: asyncio.Queue = asyncio.Queue()
                await pending_q.put(root_leaf)

                async def _leaf_worker(
                    agent: BranchingRolloutAgent,
                    url: str,
                ) -> None:
                    while True:
                        leaf = await pending_q.get()
                        try:
                            if leaf is None:
                                return
                            await agent._run_leaf_to_terminal(
                                leaf,
                                task=task["instruction"],
                                server_url=url,
                                screenshots_dir=screenshots_dir,
                                pending=pending_q,
                                terminals=terminals,
                                verify_fn=verify_fn,
                            )
                        finally:
                            pending_q.task_done()

                leaf_worker_tasks = [
                    asyncio.create_task(_leaf_worker(agent, url))
                    for agent, url, _proc in worker_specs
                ]
                await pending_q.join()
                for _ in leaf_worker_tasks:
                    await pending_q.put(None)
                await asyncio.gather(*leaf_worker_tasks)

            leaf_results: list[dict] = []
            qd_admissions: list[dict] = []
            verify_q: asyncio.Queue = asyncio.Queue()
            for leaf in terminals:
                await verify_q.put(leaf)

            async def _verify_worker(
                agent: BranchingRolloutAgent,
                url: str,
            ) -> None:
                while True:
                    leaf = await verify_q.get()
                    try:
                        if leaf is None:
                            return
                        if leaf.discarded:
                            passed = False
                            verifier_message = (
                                "Leaf discarded before final verification: "
                                f"{leaf.discard_reason or 'no reason recorded'}"
                            )
                        else:
                            passed, verifier_message = await agent._verify_leaf(
                                leaf, server_url=url, verify_fn=verify_fn,
                            )
                        admission = None
                        if self.archive is not None:
                            admission = self.archive.admit(
                                task_id=task["id"],
                                passed=passed,
                                trajectory=self._leaf_payload(leaf, task_dir),
                            )
                            qd_admissions.append({
                                "leaf_id": leaf.leaf_id,
                                **admission,
                            })
                        leaf_result = {
                            "leaf_id": leaf.leaf_id,
                            "parent_id": leaf.parent_id,
                            "role": leaf.role,
                            "fork_reason": leaf.fork_reason,
                            "discarded": leaf.discarded,
                            "discard_reason": leaf.discard_reason,
                            "passed": passed,
                            "verifier_message": verifier_message,
                            "steps": leaf.steps,
                            "is_done": leaf.is_done,
                            "final_result": leaf.final_result,
                            "teacher_interventions": leaf.teacher_interventions,
                            "errors": leaf.errors,
                            "qd_admission": admission,
                        }
                        leaf_results.append(leaf_result)
                        leaves_dir.mkdir(parents=True, exist_ok=True)
                        (leaves_dir / f"{leaf.leaf_id}.json").write_text(json.dumps({
                            **leaf_result,
                            "history": leaf.history,
                            "teacher_decisions": leaf.teacher_decisions,
                            "actions_per_step": leaf.executed_per_step,
                            "branches": leaf.branch_records,
                        }, indent=2))
                    finally:
                        verify_q.task_done()

            verify_worker_tasks = [
                asyncio.create_task(_verify_worker(agent, url))
                for agent, url, _proc in worker_specs
            ]
            await verify_q.join()
            for _ in verify_worker_tasks:
                await verify_q.put(None)
            await asyncio.gather(*verify_worker_tasks)
        finally:
            for task_obj in [*leaf_worker_tasks, *verify_worker_tasks]:
                if not task_obj.done():
                    task_obj.cancel()
            if leaf_worker_tasks or verify_worker_tasks:
                try:
                    await asyncio.wait_for(
                        asyncio.gather(
                            *leaf_worker_tasks,
                            *verify_worker_tasks,
                            return_exceptions=True,
                        ),
                        timeout=BRANCH_TASK_CANCEL_TIMEOUT,
                    )
                except asyncio.TimeoutError:
                    rollout_errors.append(
                        "branch worker task cancellation timed out"
                    )
            for worker, _url, proc in worker_specs[1:]:
                try:
                    await asyncio.wait_for(
                        worker.teardown(),
                        timeout=BRANCH_AGENT_TEARDOWN_TIMEOUT,
                    )
                except Exception as e:
                    rollout_errors.append(f"branch worker teardown failed: {e}")
                finally:
                    if proc is not None:
                        from server import stop_server
                        stop_server(proc)

        leaf_results.sort(key=lambda r: r["leaf_id"])
        qd_admissions.sort(key=lambda r: r["leaf_id"])

        passed_leaves = [r for r in leaf_results if r["passed"]]
        if passed_leaves:
            best_leaf = min(passed_leaves, key=lambda r: r["steps"])
        elif leaf_results:
            best_leaf = max(leaf_results, key=lambda r: r["steps"])
        else:
            best_leaf = None

        all_errors: list[str] = list(rollout_errors)
        for r in leaf_results:
            all_errors.extend(f"{r['leaf_id']}: {e}" for e in r.get("errors", []))

        all_teacher_decisions = []
        all_branches = []
        for leaf in terminals:
            all_teacher_decisions.extend(leaf.teacher_decisions)
            all_branches.extend(leaf.branch_records)

        self._teacher_decisions = all_teacher_decisions
        self._teacher_interventions = sum(
            leaf.teacher_interventions for leaf in terminals
        )
        self._last_traj_payload = (
            self._leaf_payload(
                next(leaf for leaf in terminals if leaf.leaf_id == best_leaf["leaf_id"]),
                task_dir,
            )
            if best_leaf and terminals else None
        )

        elapsed = round(time.time() - t0, 1)
        passed = bool(passed_leaves)
        verifier_summary = (
            f"{len(passed_leaves)}/{len(leaf_results)} leaves passed"
            if leaf_results else "0/0 leaves passed"
        )
        if best_leaf:
            verifier_summary += (
                f"; best={best_leaf['leaf_id']}: "
                f"{best_leaf['verifier_message']}"
            )
        forks_used = self._coord().forks_used

        history_payload = {
            "format": "branching_rollout",
            "leaves": leaf_results,
            "forks_used": forks_used,
            "max_forks": self.max_forks,
            "max_leaves": self.max_leaves,
            "branch_workers": len(worker_specs),
        }
        (task_dir / "history.json").write_text(json.dumps(history_payload, indent=2))
        (task_dir / "rollout_meta.json").write_text(json.dumps({
            "algorithm": "branching_src",
            "K": self.K,
            "max_forks": self.max_forks,
            "max_leaves": self.max_leaves,
            "branch_workers": len(worker_specs),
            "parallel_branching": len(worker_specs) > 1,
            "forks_used": forks_used,
            "num_leaves": len(leaf_results),
            "num_passed_leaves": len(passed_leaves),
            "teacher_interventions_total": self._teacher_interventions,
            "teacher_decisions": all_teacher_decisions,
            "branches": all_branches,
            "qd_admissions": qd_admissions,
        }, indent=2))

        return {
            "task_id": task["id"],
            "difficulty": task.get("difficulty", ""),
            "instruction": task["instruction"],
            "passed": passed,
            "verifier_message": verifier_summary,
            "elapsed": elapsed,
            "steps": best_leaf["steps"] if best_leaf else 0,
            "is_done": best_leaf["is_done"] if best_leaf else False,
            "final_result": best_leaf["final_result"] if best_leaf else None,
            "errors": all_errors,
            "branching": True,
            "num_leaves": len(leaf_results),
            "num_passed_leaves": len(passed_leaves),
            "branch_workers": len(worker_specs),
            "forks_used": forks_used,
            "total_leaf_steps": sum(r["steps"] for r in leaf_results),
            "teacher_interventions": self._teacher_interventions,
            "best_leaf_id": best_leaf["leaf_id"] if best_leaf else None,
            "leaves": leaf_results,
            "qd_admissions": qd_admissions,
        }
