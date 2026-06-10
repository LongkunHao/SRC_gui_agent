"""Teacher segment-review module for Speculative Rollback Correction.

The teacher receives a K-step student branch (per-step screenshot, thought,
action) plus the post-branch screenshot, and decides whether to:
  - accept the branch as locally progress-making, or
  - rollback to the first harmful step within the branch and emit a
    corrective action that should replace the student's choice there.

The teacher is queried via an OpenAI-compatible chat completion endpoint
(typically a vLLM server). It is asked to return a strict JSON object so
parsing is reliable even when the underlying model is a chatty VL model.

Returned ``TeacherDecision`` is consumed by ``rollout_agent`` to drive the
rollback/replay loop.
"""

from __future__ import annotations

import asyncio
import base64
import io
import json
import os
import re
from dataclasses import dataclass, field
from pathlib import Path

from openai import OpenAI
from PIL import Image, ImageDraw, ImageFont


def _env_int(name: str, default: int) -> int:
    try:
        return int(os.environ.get(name, default))
    except (TypeError, ValueError):
        return default


def _annotate_screenshot(png_b64: str, action_dicts: list[dict],
                         step_label: str) -> str:
    """Overlay action annotations on a screenshot.

    Draws:
      - large red target for click/hover/move/double_click at (x, y)
      - orange arrow through the image center for scroll, length scaled by
        |pixels|
      - small text caption in the top-left summarizing the action(s)

    Returns a new base64-encoded PNG.
    """
    try:
        img = Image.open(io.BytesIO(base64.b64decode(png_b64))).convert("RGB")
    except Exception:
        return png_b64
    draw = ImageDraw.Draw(img, "RGBA")
    W, H = img.size
    try:
        font = ImageFont.truetype(
            "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 22)
    except Exception:
        font = ImageFont.load_default()

    for a in action_dicts or []:
        t = a.get("type")
        if t in ("click", "double_click", "hover", "move") and \
                "x" in a and "y" in a:
            x, y = int(a["x"]), int(a["y"])
            r = 46
            draw.ellipse([x - r, y - r, x + r, y + r],
                         fill=(255, 0, 0, 45),
                         outline=(255, 0, 0, 255), width=8)
            draw.ellipse([x - 12, y - 12, x + 12, y + 12],
                         fill=(255, 0, 0, 255))
            draw.line([(x - r - 12, y), (x + r + 12, y)],
                      fill=(255, 0, 0, 230), width=5)
            draw.line([(x, y - r - 12), (x, y + r + 12)],
                      fill=(255, 0, 0, 230), width=5)
        elif t == "scroll":
            try:
                amount = max(1, int(a.get("amount", 3)))
            except (ValueError, TypeError):
                amount = 3
            direction = a.get("direction", "down")
            # Arrow magnitude scales with amount (capped to viewport).
            mag = min(int(H * 0.45),
                      max(int(H * 0.10), amount * int(H * 0.05)))
            cx, cy = W // 2, H // 2
            if direction == "down":
                y0, y1 = cy - mag // 2, cy + mag // 2
            else:
                y0, y1 = cy + mag // 2, cy - mag // 2
            draw.line([(cx, y0), (cx, y1)],
                      fill=(255, 165, 0, 255), width=8)
            # Arrow head
            head = 18
            if y1 > y0:  # pointing down
                draw.polygon([(cx, y1 + head),
                              (cx - head, y1 - 2),
                              (cx + head, y1 - 2)],
                             fill=(255, 165, 0, 255))
            else:  # pointing up
                draw.polygon([(cx, y1 - head),
                              (cx - head, y1 + 2),
                              (cx + head, y1 + 2)],
                             fill=(255, 165, 0, 255))
        elif t == "input":
            pass
        elif t == "key":
            pass
        elif t == "terminate":
            pass
        else:
            pass

    buf = io.BytesIO()
    img.save(buf, format="PNG", optimize=True)
    return base64.b64encode(buf.getvalue()).decode()


_TEACHER_SYSTEM_PROMPT_PATH = Path(
    os.environ.get(
        "TEACHER_SYSTEM_PROMPT_PATH",
        Path(__file__).parent / "prompts" / "teacher_review_prompt.md",
    )
)


def _load_teacher_system_prompt() -> str:
    return _TEACHER_SYSTEM_PROMPT_PATH.read_text(encoding="utf-8").strip()


@dataclass
class TeacherDecision:
    accept: bool
    rollback_to: int = 0          # offset in branch (0..K-1)
    reason: str = ""
    correction: dict | None = None  # raw teacher tool params (computer_use schema)
    raw: str = ""
    error: str | None = None

    def to_record(self) -> dict:
        return {
            "accept": self.accept,
            "rollback_to": self.rollback_to,
            "reason": self.reason,
            "correction": self.correction,
            "error": self.error,
        }


@dataclass
class BranchStep:
    """One executed student step inside a K-step branch."""
    index_in_branch: int
    screenshot_b64: str            # screenshot the student saw BEFORE acting
    thought: str
    action_summary: str
    action_dicts: list[dict] = field(default_factory=list)


@dataclass
class ReviewContextStep:
    """A pre-branch step shown only as context for teacher review."""
    absolute_step: int
    screenshot_b64: str            # screenshot observed BEFORE acting
    action_summary: str
    action_dicts: list[dict] = field(default_factory=list)


class TeacherReviewer:
    """Wraps an OpenAI-compatible vision-LLM client used as the teacher."""

    def __init__(
        self,
        *,
        base_url: str | None = None,
        api_key: str | None = None,
        model: str | None = None,
        max_tokens: int = 19200,
        temperature: float = 0.0,
        review_context_steps: int | None = None,
        correction_image_max: int | None = None,
    ):
        self.base_url = base_url or os.environ.get(
            "TEACHER_BASE_URL", "http://localhost:9002/v1"
        )
        self.api_key = api_key or os.environ.get("TEACHER_API_KEY", "EMPTY")
        self.model = model or os.environ.get("TEACHER_MODEL", "Qwen3.6-27B")
        self.max_tokens = max_tokens
        self.temperature = temperature
        self.review_context_steps = (
            review_context_steps
            if review_context_steps is not None
            else _env_int("TEACHER_REVIEW_CONTEXT_STEPS", 4)
        )
        self.correction_image_max = (
            correction_image_max
            if correction_image_max is not None
            else _env_int("TEACHER_CORRECTION_IMAGE_MAX", 6)
        )
        self._client = OpenAI(api_key=self.api_key, base_url=self.base_url)
        # Optional per-task LLM tracer; set by the caller (e.g. RolloutAgent).
        self.tracer = None
        self._llm_image_counter = 0

    # ------------------------------------------------------------------ API

    async def review(
        self,
        *,
        task: str,
        server_url: str,
        branch_start: int = 0,
        branch: list[BranchStep],
        post_branch_screenshot_b64: str,
        accepted_prefix: list[ReviewContextStep] | None = None,
        verifier_feedback: dict | None = None,
    ) -> TeacherDecision:
        """First shot: accept-or-rollback decision (NO correction).

        The corrective action is solicited separately via
        ``review_correction`` after the env has been rolled back, so the
        teacher can see the actual rolled-back screen instead of inferring
        it from the K-step branch.
        """
        messages = self._build_messages(
            task=task,
            server_url=server_url,
            branch_start=branch_start,
            branch=branch,
            post_branch_screenshot_b64=post_branch_screenshot_b64,
            accepted_prefix=accepted_prefix or [],
            verifier_feedback=verifier_feedback,
        )
        try:
            content = await self._call(messages, call_type="teacher_review")
        except Exception as e:  # network / API failure → default to accept
            return TeacherDecision(accept=True, reason=f"teacher error: {e}",
                                   error=str(e))
        return self._parse(content, k=len(branch))

    async def review_correction(
        self,
        *,
        messages: list[dict],
    ) -> str:
        """Second shot: caller (rollout_agent) builds a Qwen-format messages
        list (same prompt as the student, with the rollback reason appended
        to the instruction).  We just send it through and return the raw
        text (XML <tool_call>...</tool_call>) so the caller can parse it
        with the existing student-side XML parser.
        """
        try:
            return await self._call(messages, call_type="teacher_correction")
        except Exception:
            return ""

    # ------------------------------------------------------------ internals

    def _build_messages(
        self,
        *,
        task: str,
        server_url: str,
        branch_start: int = 0,
        branch: list[BranchStep],
        post_branch_screenshot_b64: str,
        accepted_prefix: list[ReviewContextStep] | None = None,
        verifier_feedback: dict | None = None,
    ) -> list[dict]:
        K = len(branch)
        prefix = accepted_prefix or []
        user_blocks: list[dict] = [
            {"type": "text",
             "text": (
                 f"Task: {task}\n"
                 f"App URL: {server_url}\n"
                 f"Branch length K = {K}\n\n"
                 f"Below are {len(prefix)} recent pre-branch context step(s), "
                 f"then the {K} student steps in order, then the screenshot taken "
                 f"AFTER the branch finished. For each branch step you see the "
                 f"screenshot the student observed BEFORE acting, plus the "
                 f"student's thought and action."
             )},
        ]
        if prefix:
            user_blocks.append({
                "type": "text",
                "text": (
                    "--- PRE-BRANCH CONTEXT (already executed before this "
                    "branch; use only as context, rollback_to must still refer "
                    "to the current branch) ---"
                ),
            })
        if verifier_feedback:
            passed = bool(verifier_feedback.get("passed"))
            message = str(verifier_feedback.get("message", ""))
            user_blocks.append({
                "type": "text",
                "text": (
                    "--- ENVIRONMENT / VERIFIER FEEDBACK AFTER THIS BRANCH ---\n"
                    f"Hard verifier result: {'PASSED' if passed else 'FAILED'}\n"
                    f"Verifier message: {message}\n"
                    "This feedback is authoritative for any terminate(success) "
                    "claim in the branch."
                ),
            })
        for c in prefix:
            annotated = _annotate_screenshot(
                c.screenshot_b64, c.action_dicts,
                f"context abs {c.absolute_step}",
            )
            self._save_llm_image(
                annotated,
                f"teacher_review_ctx_abs{c.absolute_step}.png",
            )
            try:
                actions_json = json.dumps(c.action_dicts, ensure_ascii=False)
            except TypeError:
                actions_json = str(c.action_dicts)
            user_blocks.append({
                "type": "text",
                "text": (
                    f"--- Context absolute step {c.absolute_step} "
                    f"(screenshot is BEFORE the action; annotation marks the "
                    f"executed action) ---"
                ),
            })
            user_blocks.append({
                "type": "image_url",
                "image_url": {"url": f"data:image/png;base64,{annotated}"},
            })
            user_blocks.append({
                "type": "text",
                "text": (
                    f"Executed action dicts: {actions_json}\n"
                    f"Action summary: {c.action_summary}"
                ),
            })
        for s in branch:
            abs_step = branch_start + s.index_in_branch
            annotated = _annotate_screenshot(
                s.screenshot_b64, s.action_dicts,
                f"abs {abs_step} / branch {s.index_in_branch}",
            )
            self._save_llm_image(
                annotated,
                f"teacher_review_abs{abs_step}_branch{s.index_in_branch}.png",
            )
            try:
                actions_json = json.dumps(s.action_dicts, ensure_ascii=False)
            except TypeError:
                actions_json = str(s.action_dicts)
            user_blocks.append({
                "type": "text",
                "text": (
                    f"--- Branch step {s.index_in_branch} / absolute step "
                    f"{abs_step} (screenshot is BEFORE the action; red "
                    f"annotation marks the executed action) ---"
                ),
            })
            user_blocks.append({
                "type": "image_url",
                "image_url": {"url": f"data:image/png;base64,{annotated}"},
            })
            user_blocks.append({
                "type": "text",
                "text": (
                    f"Executed action dicts: {actions_json}\n"
                    f"Student action line: {s.action_summary}\n"
                    f"Student thought (may be wrong): {s.thought}"
                ),
            })
        post_annotated = _annotate_screenshot(
            post_branch_screenshot_b64, [], "post branch",
        )
        self._save_llm_image(
            post_annotated,
            f"teacher_review_post_branch_start{branch_start}.png",
        )
        user_blocks.append({"type": "text",
                            "text": "--- Screenshot AFTER the K-step branch ---"})
        user_blocks.append({
            "type": "image_url",
            "image_url": {"url": f"data:image/png;base64,{post_annotated}"},
        })
        user_blocks.append({"type": "text",
                            "text": "Now respond with the JSON object only."})

        return [
            {"role": "system", "content": _load_teacher_system_prompt()},
            {"role": "user", "content": user_blocks},
        ]

    def _save_llm_image(self, png_b64: str, filename: str) -> None:
        tracer = self.tracer
        if tracer is None or not hasattr(tracer, "save_b64_image"):
            return
        self._llm_image_counter += 1
        safe_name = f"{self._llm_image_counter:04d}_{filename}"
        try:
            tracer.save_b64_image(png_b64, f"llm_images/{safe_name}")
        except Exception:
            pass

    async def _call(self, messages: list[dict], *,
                    call_type: str = "teacher") -> str:
        def _do():
            resp = self._client.chat.completions.create(
                model=self.model,
                messages=messages,
                max_tokens=self.max_tokens,
                temperature=self.temperature,
                top_p=0.9,
                extra_body={
                    "chat_template_kwargs": {"enable_thinking": False},
                },
            )
            return resp.choices[0].message.content or ""
        try:
            content = await asyncio.to_thread(_do)
        except Exception as e:
            tracer = self.tracer
            if tracer is not None:
                try:
                    tracer.log(
                        call_type=call_type,
                        model=self.model,
                        messages=messages,
                        response="",
                        error=str(e),
                    )
                except Exception:
                    pass
            raise
        tracer = self.tracer
        if tracer is not None:
            try:
                tracer.log(
                    call_type=call_type,
                    model=self.model,
                    messages=messages,
                    response=content,
                )
            except Exception:
                pass
        return content

    @staticmethod
    def _parse(content: str, *, k: int) -> TeacherDecision:
        # Strip code fences if present, then grab first {...} JSON object.
        text = content.strip()
        text = re.sub(r"^```(?:json)?\s*|\s*```$", "", text, flags=re.MULTILINE)
        m = re.search(r"\{.*\}", text, re.DOTALL)
        if not m:
            return TeacherDecision(accept=True, raw=content,
                                   reason="no JSON in teacher response",
                                   error="parse")
        try:
            obj = json.loads(m.group(0))
        except json.JSONDecodeError as e:
            return TeacherDecision(accept=True, raw=content,
                                   reason=f"bad JSON: {e}", error="parse")

        accept = bool(obj.get("accept", True))
        rb = int(obj.get("rollback_to", 0) or 0)
        rb = max(0, min(rb, max(0, k - 1)))
        reason = str(obj.get("reason", ""))[:400]
        # NOTE: correction is no longer returned by the first-shot prompt;
        # it is solicited via review_correction(...) after the env rollback.
        return TeacherDecision(
            accept=accept,
            rollback_to=rb,
            reason=reason,
            correction=None,
            raw=content,
        )
