"""Quality-Diversity archive for verifier-passing trajectories.

Stores at most three trajectories per (task_id, descriptor-bin). Descriptors:
  - path_length bucket (≤ K, K..2K, 2K..3K, 3K+)
  - dominant action-type bucket (most-used action type among click / type / scroll / key / other)
  - teacher_intervention_count bucket (0, 1, 2, 3+)

Quality gates (a trajectory is rejected outright if it fails any gate):
  - verifier passed
  - path_length ≤ ``max_length``
  - max consecutive identical actions ≤ ``max_repeat``
  - teacher_interventions ≤ ``max_interventions``
"""

from __future__ import annotations

import json
import threading
import uuid
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path


def _action_type_dist(actions_per_step: list[list[dict]]) -> dict:
    c: Counter = Counter()
    for step_actions in actions_per_step:
        for a in step_actions:
            c[a.get("type", "unknown")] += 1
    return dict(c)


def _dominant_bucket(dist: dict) -> str:
    if not dist:
        return "none"
    top = max(dist.items(), key=lambda kv: kv[1])[0]
    if top in ("click", "double_click"):
        return "click"
    if top in ("input",):
        return "type"
    if top in ("scroll",):
        return "scroll"
    if top in ("key",):
        return "key"
    return "other"


def _length_bucket(n: int) -> str:
    if n <= 5:
        return "lenA_short"
    if n <= 12:
        return "lenB_medium"
    if n <= 25:
        return "lenC_long"
    return "lenD_xlong"


def _intervention_bucket(n: int) -> str:
    if n == 0:
        return "int0"
    if n == 1:
        return "int1"
    if n == 2:
        return "int2"
    return "int3plus"


def _max_consecutive_repeat(actions_per_step: list[list[dict]]) -> int:
    sigs = []
    for step_actions in actions_per_step:
        for a in step_actions:
            text = a.get("text", "")
            text_prefix = text[:20] if isinstance(text, str) else ""
            # Include enough fields to distinguish scroll/key variants:
            # without direction/amount, two scrolls in opposite directions
            # look identical; without keys, Enter/Tab/ArrowDown collapse
            # into one signature and trip the repeat gate.
            sig = (
                a.get("type"),
                a.get("x"),
                a.get("y"),
                a.get("button"),
                a.get("direction"),
                a.get("amount"),
                a.get("keys"),
                text_prefix,
            )
            sigs.append(sig)
    best = cur = 0
    last = None
    for s in sigs:
        if s == last:
            cur += 1
        else:
            cur = 1
            last = s
        best = max(best, cur)
    return best


class QDArchive:
    """Thread-safe per-task QD archive backed by the filesystem."""

    def __init__(
        self,
        root: Path,
        *,
        max_length: int = 60,
        max_repeat: int = 4,
        max_interventions: int = 6,
    ):
        self.root = Path(root)
        self.root.mkdir(parents=True, exist_ok=True)
        self.max_length = max_length
        self.max_repeat = max_repeat
        self.max_interventions = max_interventions
        self._lock = threading.Lock()

    def admit(
        self,
        *,
        task_id: str,
        passed: bool,
        trajectory: dict,
        quality_score: float | None = None,
    ) -> dict:
        """Try to add ``trajectory`` to the archive.

        ``trajectory`` must include keys: ``actions_per_step`` (list[list[dict]]),
        ``teacher_interventions`` (int), and any extra payload to persist.

        ``quality_score`` is an optional caller-supplied scalar (higher is
        better). When present it dominates the in-bin ranking, so future
        reward/quality models can plug straight in without changing this
        module.

        Returns a small dict describing the admission decision (admitted/bin/...).
        """
        actions_per_step = trajectory.get("actions_per_step", [])
        n_steps = len(actions_per_step)
        n_int = int(trajectory.get("teacher_interventions", 0))
        dist = _action_type_dist(actions_per_step)
        max_rep = _max_consecutive_repeat(actions_per_step)

        gates = {
            "verifier_passed": passed,
            "length_ok": n_steps <= self.max_length,
            "repeat_ok": max_rep <= self.max_repeat,
            "intervention_ok": n_int <= self.max_interventions,
        }
        if not all(gates.values()):
            return {"admitted": False, "gates": gates,
                    "reason": "quality gate", "stats": {
                        "steps": n_steps, "max_repeat": max_rep,
                        "interventions": n_int}}

        bin_id = "__".join([
            _length_bucket(n_steps),
            _dominant_bucket(dist),
            _intervention_bucket(n_int),
        ])
        out_dir = self.root / task_id / bin_id
        out_dir.mkdir(parents=True, exist_ok=True)
        index_file = out_dir / "index.json"

        # Spread ``trajectory`` first so the archive's own computed fields
        # (task_id, bin, n_steps, ...) cannot be silently overwritten by a
        # caller-supplied trajectory dict that happens to carry the same
        # key names.
        payload = {
            **trajectory,
            "task_id": task_id,
            "bin": bin_id,
            "n_steps": n_steps,
            "teacher_interventions": n_int,
            "action_type_distribution": dist,
            "max_consecutive_repeat": max_rep,
            "quality_score": quality_score,
            "trajectory_id": uuid.uuid4().hex,
            "created_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        }

        with self._lock:
            existing = []
            if index_file.exists():
                try:
                    existing = json.loads(index_file.read_text())
                except json.JSONDecodeError:
                    existing = []
            # Keep at most 3 trajectories per (task, bin). Ranking:
            #   1. higher quality_score wins (None treated as -inf)
            #   2. shorter trajectory wins
            #   3. fewer teacher interventions wins
            #   4. older entries win on exact ties (stable insertion order)
            existing.append(payload)

            def _sort_key(r: dict) -> tuple:
                qs = r.get("quality_score")
                qs_rank = -qs if isinstance(qs, (int, float)) else float("inf")
                return (qs_rank, r["n_steps"], r["teacher_interventions"])

            existing.sort(key=_sort_key)
            existing = existing[:3]
            index_file.write_text(json.dumps(existing, indent=2))

        return {"admitted": True, "bin": bin_id, "gates": gates,
                "trajectory_id": payload["trajectory_id"],
                "stats": {"steps": n_steps, "max_repeat": max_rep,
                          "interventions": n_int,
                          "quality_score": quality_score}}
