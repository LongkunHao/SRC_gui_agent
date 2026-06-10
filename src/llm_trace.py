"""Per-task LLM call tracer.

Writes every student / teacher LLM request + response to one JSONL file
under the task directory so a human can replay or diff prompts when
debugging.  All input images are already saved by the agent under
``{task_dir}/screenshots/``; callers register each screenshot's bytes
with the tracer right after writing it, and the tracer rewrites inline
``image_url`` data URIs to ``{"type":"image_ref","path":"screenshots/..."}``
references via a direct dict lookup (no hashing).

One file per task:
    {task_dir}/llm_calls.jsonl
"""

from __future__ import annotations

import base64
import json
import threading
import time
from pathlib import Path


class LLMTracer:
    def __init__(self, task_dir: Path):
        self.task_dir = Path(task_dir)
        self.task_dir.mkdir(parents=True, exist_ok=True)
        self.path = self.task_dir / "llm_calls.jsonl"
        self._lock = threading.Lock()
        self._step = 0  # monotonic call counter
        # b64 string of a registered screenshot -> path relative to task_dir.
        # Caller invokes ``register(bytes, screenshot_path)`` after writing.
        self._b64_to_path: dict[str, str] = {}

    # ---------------------------------------------------------------- register

    def register(self, screenshot_bytes: bytes, path: Path | str) -> None:
        """Record that ``screenshot_bytes`` was saved at ``path``.

        Subsequent LLM messages that include this exact byte sequence
        (as a base64 data URI) will be rewritten to reference ``path``.
        ``path`` may be absolute (under task_dir) or relative.
        """
        if not screenshot_bytes:
            return
        p = Path(path)
        try:
            rel = str(p.relative_to(self.task_dir))
        except ValueError:
            rel = str(p)
        b64 = base64.b64encode(screenshot_bytes).decode("ascii")
        # Keep the first registered path stable. The same screenshot bytes
        # can be saved under multiple names during rollback; overwriting the
        # mapping makes old LLM calls appear to reference later screenshots.
        self._b64_to_path.setdefault(b64, rel)

    def save_b64_image(self, png_b64: str, path: Path | str) -> str:
        """Save a base64 PNG under task_dir and register it for logging.

        Returns the path relative to task_dir when possible.
        """
        data = base64.b64decode(png_b64)
        p = Path(path)
        out_path = p if p.is_absolute() else self.task_dir / p
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_bytes(data)
        self.register(data, out_path)
        try:
            return str(out_path.relative_to(self.task_dir))
        except ValueError:
            return str(out_path)

    # ---------------------------------------------------------------- helpers

    def _strip_messages(self, messages):
        """Replace inline image data URIs with relative file refs."""
        out = []
        for m in messages or []:
            content = m.get("content") if isinstance(m, dict) else None
            role = m.get("role") if isinstance(m, dict) else None
            if isinstance(content, list):
                new_content = []
                for c in content:
                    if isinstance(c, dict) and c.get("type") == "image_url":
                        url = ""
                        if isinstance(c.get("image_url"), dict):
                            url = c["image_url"].get("url", "") or ""
                        elif isinstance(c.get("image_url"), str):
                            url = c["image_url"]
                        if isinstance(url, str) and url.startswith("data:"):
                            b64 = url.split(",", 1)[1] if "," in url else url
                            ref = self._b64_to_path.get(b64, "<unregistered>")
                            new_content.append({
                                "type": "image_ref",
                                "path": ref,
                            })
                            continue
                    new_content.append(c)
                out.append({"role": role, "content": new_content})
            else:
                out.append({"role": role, "content": content})
        return out

    # -------------------------------------------------------------------- log

    def log(
        self,
        *,
        call_type: str,
        model: str,
        messages,
        response: str = "",
        error: str | None = None,
        extra: dict | None = None,
    ) -> None:
        with self._lock:
            self._step += 1
            idx = self._step
        record = {
            "idx": idx,
            "ts": round(time.time(), 3),
            "call_type": call_type,
            "model": model,
            "messages": self._strip_messages(messages),
            "response": response,
        }
        if error:
            record["error"] = error
        if extra:
            record["extra"] = extra
        line = json.dumps(record, ensure_ascii=False)
        with self._lock:
            with open(self.path, "a", encoding="utf-8") as f:
                f.write(line + "\n")
