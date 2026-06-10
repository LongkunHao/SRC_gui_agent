#!/usr/bin/env python3
"""Rich terminal dashboard for monitoring Mirror-Mirror pipeline instances.

Polls instances in parallel via SSH, parses pipeline logs for structured
phase/iteration/pass-rate history, and renders one card per environment.

Usage:
    python infra/setup/dashboard.py                     # live dashboard, 30s refresh
    python infra/setup/dashboard.py --interval 15       # faster refresh
    python infra/setup/dashboard.py --once              # single snapshot, exit
    python infra/setup/dashboard.py --log ENV_ID        # tail last 50 log lines
    python infra/setup/dashboard.py --log-lines 100     # more log lines with --log
    python infra/setup/dashboard.py --launch-env PATH   # custom launch file path
"""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path

try:
    from rich.console import Console, Group
    from rich.panel import Panel
    from rich.text import Text
except ImportError:
    print("ERROR: 'rich' library required. Install: uv pip install rich")
    sys.exit(1)


# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

PHASE_ORDER = [
    "phase_1", "phase_2a", "phase_2b",
    "phase_3a", "phase_3b",
    "phase_4", "phase_5",
]

PHASE_DISPLAY = {
    "phase_1":  ("Phase 1 ", "Generate App"),
    "phase_2a": ("Phase 2a", "Gen Function Tasks"),
    "phase_2b": ("Phase 2b", "Fn Eval-Audit"),
    "phase_3a": ("Phase 3a", "Gen Real Tasks"),
    "phase_3b": ("Phase 3b", "Real Eval-Audit"),
    "phase_4":  ("Phase 4 ", "Hardening"),
    "phase_5":  ("Phase 5 ", "Final Eval"),
}

INDICATORS = {
    "complete": ("\u2713", "green"),
    "running":  ("\u25cf", "yellow"),
    "pending":  ("\u25cb", "dim"),
    "failed":   ("\u2717", "red"),
    "skipped":  ("\u2013", "dim"),
}

STATUS_SORT = {
    "running": 0,
    "failed": 1,
    "stopped": 1,
    "setting_up": 2,
    "not_started": 2,
    "ssh_error": 3,
    "complete": 4,
    "unknown": 5,
}

# Single compound SSH command per instance — collects everything in one trip.
REMOTE_SCRIPT = r'''
echo "SETUP:$(test -f ~/.setup-complete && echo yes || echo no)"
echo "RUNNING:$(pgrep -f 'infra/pipeline[.]py' > /dev/null 2>&1 && echo yes || echo no)"
echo "TIME:$(date +%s)"
STATE=$(cat ~/mirror-mirror/logs/*/pipeline_state.json 2>/dev/null || echo null)
echo "STATE_JSON:$STATE"
echo "LOG_START"
grep -E '(Phase [0-9]|pass rate|Pipeline complete|Pipeline starting|Hardening round|Generated .* new tasks|Audit made no changes|All .* passed|No new tasks generated)' /tmp/mirror-mirror-logs/pipeline.log 2>/dev/null | tail -200
echo "LOG_END"
'''.strip()


# ---------------------------------------------------------------------------
# Dataclasses
# ---------------------------------------------------------------------------

@dataclass
class PhaseHistory:
    """Tracks pass rates and status for one pipeline phase."""
    status: str = "pending"  # complete | running | pending | failed | skipped
    iterations: list[dict] = field(default_factory=list)   # phase 2b/3b
    rounds: list[dict] = field(default_factory=list)       # phase 4
    final_fn_rate: float | None = None                     # phase 5
    final_real_rate: float | None = None                   # phase 5
    current_iter: int = 0
    max_iter: int = 0
    current_round: int = 0
    max_rounds: int = 0


@dataclass
class InstanceInfo:
    """Static instance info parsed from launch.env."""
    env_id: str
    instance_id: str
    ip: str
    eip_alloc_id: str = ""


@dataclass
class InstanceStatus:
    """Full status of one pipeline instance after polling."""
    env_id: str
    instance_id: str
    ip: str
    setup_complete: bool = False
    pipeline_running: bool = False
    ssh_error: bool = False
    state_json: dict | None = None
    phase_history: dict[str, PhaseHistory] = field(default_factory=dict)
    started_at: datetime | None = None
    remote_now: datetime | None = None
    overall_status: str = "unknown"
    hardening_rounds: int = 3


# ---------------------------------------------------------------------------
# Launch env parsing
# ---------------------------------------------------------------------------

def parse_launch_env(path: str) -> tuple[dict[str, str], list[InstanceInfo]]:
    """Parse the launch.env file created by launch.sh.

    Returns (config_dict, list_of_instances).
    """
    config: dict[str, str] = {}
    instances: list[InstanceInfo] = []

    with open(path) as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            # Per-instance detail: # env_id|instance_id|ip|eip_alloc_id
            if line.startswith("#") and "|" in line:
                parts = line.lstrip("# ").split("|")
                # Validate: need 3+ fields, IP must look like an IP (digits+dots)
                if len(parts) >= 3 and re.match(r"[\d.]+$", parts[2].strip()):
                    instances.append(InstanceInfo(
                        env_id=parts[0].strip(),
                        instance_id=parts[1].strip(),
                        ip=parts[2].strip(),
                        eip_alloc_id=parts[3].strip() if len(parts) > 3 else "",
                    ))
                continue
            if line.startswith("#"):
                continue
            # KEY=VALUE or KEY="VALUE"
            if "=" in line:
                key, _, val = line.partition("=")
                config[key.strip()] = val.strip().strip('"').strip("'")

    return config, instances


# ---------------------------------------------------------------------------
# Log parsing
# ---------------------------------------------------------------------------

def _ensure_done(status: str) -> str:
    """Mark a phase complete if it was running/pending (implied by next phase)."""
    if status in ("running", "pending"):
        return "complete"
    return status


def _utc_from_epoch(epoch: int) -> datetime:
    """Convert epoch seconds to naive UTC datetime."""
    return datetime.fromtimestamp(epoch, tz=timezone.utc).replace(tzinfo=None)


def parse_log_lines(
    lines: list[str],
) -> tuple[dict[str, PhaseHistory], datetime | None]:
    """Parse structured log lines into per-phase history.

    Returns (phase_history_dict, started_at_datetime).
    """
    phases: dict[str, PhaseHistory] = {k: PhaseHistory() for k in PHASE_ORDER}
    started_at: datetime | None = None
    pipeline_complete = False

    for raw_line in lines:
        # Format: "2026-02-16 14:35:02 [pipeline] Phase 2b: ..."
        ts_match = re.match(
            r"(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}) \[pipeline\] (.*)", raw_line,
        )
        if ts_match:
            ts_str, msg = ts_match.group(1), ts_match.group(2)
            try:
                ts = datetime.strptime(ts_str, "%Y-%m-%d %H:%M:%S")
            except ValueError:
                ts = None
        else:
            msg = raw_line.strip()
            ts = None

        # --- Pipeline lifecycle ---
        if "Pipeline starting for:" in msg:
            started_at = ts
            continue
        if "Pipeline complete for:" in msg:
            pipeline_complete = True
            continue

        # --- Phase 1 ---
        if "Phase 1: Generating web app" in msg:
            phases["phase_1"].status = "running"
        elif "Phase 1 complete" in msg:
            phases["phase_1"].status = "complete"
        elif "Phase 1 FAILED" in msg:
            phases["phase_1"].status = "failed"
        elif "Phase 1: Skipped" in msg:
            phases["phase_1"].status = "skipped"

        # --- Phase 2 ---
        elif "Phase 2: Skipped" in msg:
            phases["phase_2a"].status = "skipped"
            phases["phase_2b"].status = "skipped"
        elif "Phase 2a: Generating function tasks" in msg:
            phases["phase_1"].status = _ensure_done(phases["phase_1"].status)
            phases["phase_2a"].status = "running"
        elif "Phase 2a: Skipped" in msg:
            phases["phase_2a"].status = "skipped"
        elif "Phase 2a FAILED" in msg:
            phases["phase_2a"].status = "failed"
        elif m := re.search(
            r"Phase 2b: Function task iteration (\d+)/(\d+)", msg,
        ):
            phases["phase_2a"].status = _ensure_done(phases["phase_2a"].status)
            phases["phase_2b"].status = "running"
            phases["phase_2b"].current_iter = int(m.group(1))
            phases["phase_2b"].max_iter = int(m.group(2))
        elif m := re.search(
            r"^Function task pass rate: ([\d.]+)% \((\d+)/(\d+)\)", msg,
        ):
            phases["phase_2b"].iterations.append({
                "pass_rate": float(m.group(1)),
                "passed": int(m.group(2)),
                "total": int(m.group(3)),
            })
        elif "Phase 2 complete" in msg:
            phases["phase_2a"].status = _ensure_done(phases["phase_2a"].status)
            phases["phase_2b"].status = "complete"

        # --- Phase 3 ---
        elif "Phase 3: Skipped" in msg:
            phases["phase_3a"].status = "skipped"
            phases["phase_3b"].status = "skipped"
        elif "Phase 3a: Generating real tasks" in msg:
            phases["phase_2a"].status = _ensure_done(phases["phase_2a"].status)
            phases["phase_2b"].status = _ensure_done(phases["phase_2b"].status)
            phases["phase_3a"].status = "running"
        elif "Phase 3a: Skipped" in msg:
            phases["phase_3a"].status = "skipped"
        elif "Phase 3a FAILED" in msg:
            phases["phase_3a"].status = "failed"
        elif m := re.search(
            r"Phase 3b: Real task iteration (\d+)/(\d+)", msg,
        ):
            phases["phase_3a"].status = _ensure_done(phases["phase_3a"].status)
            phases["phase_3b"].status = "running"
            phases["phase_3b"].current_iter = int(m.group(1))
            phases["phase_3b"].max_iter = int(m.group(2))
        elif m := re.search(
            r"^Real task pass rate: ([\d.]+)% \((\d+)/(\d+)\)", msg,
        ):
            phases["phase_3b"].iterations.append({
                "pass_rate": float(m.group(1)),
                "passed": int(m.group(2)),
                "total": int(m.group(3)),
            })
        elif "Phase 3 complete" in msg:
            phases["phase_3a"].status = _ensure_done(phases["phase_3a"].status)
            phases["phase_3b"].status = "complete"

        # --- Phase 4 ---
        elif m := re.search(r"Phase 4: Task hardening \((\d+) rounds", msg):
            phases["phase_4"].status = "running"
            phases["phase_4"].max_rounds = int(m.group(1))
        elif m := re.search(r"Phase 4: Hardening round (\d+)/(\d+)", msg):
            phases["phase_4"].status = "running"
            phases["phase_4"].current_round = int(m.group(1))
            phases["phase_4"].max_rounds = int(m.group(2))
        elif m := re.search(
            r"Hardening round (\d+) eval: ([\d.]+)% \((\d+)/(\d+)\)", msg,
        ):
            round_num = int(m.group(1))
            entry = {
                "round": round_num,
                "pass_rate": float(m.group(2)),
                "passed": int(m.group(3)),
                "total": int(m.group(4)),
            }
            # Extend list to accommodate this round number
            while len(phases["phase_4"].rounds) < round_num:
                phases["phase_4"].rounds.append({})
            phases["phase_4"].rounds[round_num - 1] = entry
        elif m := re.search(
            r"Post-audit eval: ([\d.]+)% \((\d+)/(\d+)\)", msg,
        ):
            # Update the most recent round with post-audit result
            if phases["phase_4"].rounds:
                phases["phase_4"].rounds[-1].update({
                    "pass_rate": float(m.group(1)),
                    "passed": int(m.group(2)),
                    "total": int(m.group(3)),
                })
        elif "Phase 4a FAILED" in msg:
            phases["phase_4"].status = "failed"
        elif "Phase 4: Skipped" in msg:
            phases["phase_4"].status = "skipped"
        elif "Phase 4 complete" in msg:
            phases["phase_4"].status = "complete"

        # --- Phase 5 ---
        elif "Phase 5: Final regression eval" in msg:
            phases["phase_5"].status = "running"
        elif m := re.search(
            r"Final function task pass rate: ([\d.]+)%", msg,
        ):
            phases["phase_5"].final_fn_rate = float(m.group(1))
        elif m := re.search(
            r"Final real task pass rate: ([\d.]+)%", msg,
        ):
            phases["phase_5"].final_real_rate = float(m.group(1))
        elif "Phase 5 complete" in msg:
            phases["phase_5"].status = "complete"
        elif "Phase 5: Skipped" in msg:
            phases["phase_5"].status = "skipped"

    # If pipeline completed, ensure all running phases are marked done
    if pipeline_complete:
        for key in PHASE_ORDER:
            if phases[key].status == "running":
                phases[key].status = "complete"

    return phases, started_at


# ---------------------------------------------------------------------------
# Progress helpers
# ---------------------------------------------------------------------------

def compute_progress(
    phases: dict[str, PhaseHistory],
    hardening_rounds: int = 3,
) -> tuple[int, int, str]:
    """Compute (completed_steps, total_steps, current_phase_label).

    Steps: phases 1-3b (5) + hardening rounds (N) + phase 5 (1).
    The count includes the currently running phase (we've "reached" that step).
    """
    total = 5 + hardening_rounds + 1
    completed = 0
    current_label = "Starting"

    # Phases 1 through 3b: 5 fixed steps
    for key in ("phase_1", "phase_2a", "phase_2b", "phase_3a", "phase_3b"):
        ph = phases.get(key, PhaseHistory())
        if ph.status in ("complete", "skipped"):
            completed += 1
        elif ph.status == "running":
            completed += 1  # count reaching this phase
            current_label = PHASE_DISPLAY[key][0].strip()
        elif ph.status == "failed":
            completed += 1
            current_label = PHASE_DISPLAY[key][0].strip()

    # Phase 4: one step per completed hardening round
    ph4 = phases.get("phase_4", PhaseHistory())
    if ph4.status in ("complete", "skipped"):
        completed += hardening_rounds
    elif ph4.status in ("running", "failed"):
        # Count completed rounds, plus 1 for starting the current round
        done_rounds = len([r for r in ph4.rounds if r])
        in_progress = 1 if ph4.current_round > done_rounds else 0
        completed += done_rounds + in_progress
        current_label = "Phase 4"

    # Phase 5
    ph5 = phases.get("phase_5", PhaseHistory())
    if ph5.status in ("complete", "skipped"):
        completed += 1
    elif ph5.status in ("running", "failed"):
        completed += 1
        current_label = "Phase 5"

    completed = min(completed, total)
    if completed >= total:
        current_label = "Done"

    return completed, total, current_label


def format_elapsed(
    started_at: datetime | None, now: datetime | None,
) -> str:
    """Format elapsed time as 'Xh YYm' or 'Ym'."""
    if not started_at or not now:
        return ""
    total_secs = int((now - started_at).total_seconds())
    if total_secs < 0:
        return ""
    hours, remainder = divmod(total_secs, 3600)
    minutes, _ = divmod(remainder, 60)
    if hours > 0:
        return f"{hours}h {minutes:02d}m"
    return f"{minutes}m"


# ---------------------------------------------------------------------------
# SSH polling
# ---------------------------------------------------------------------------

def poll_instance(inst: InstanceInfo, ssh_key_path: str) -> InstanceStatus:
    """SSH into one instance and collect full status."""
    status = InstanceStatus(
        env_id=inst.env_id,
        instance_id=inst.instance_id,
        ip=inst.ip,
    )

    cmd = [
        "ssh",
        "-i", ssh_key_path,
        "-o", "StrictHostKeyChecking=no",
        "-o", "ConnectTimeout=10",
        "-o", "BatchMode=yes",
        f"ec2-user@{inst.ip}",
        REMOTE_SCRIPT,
    ]

    try:
        result = subprocess.run(
            cmd, capture_output=True, text=True, timeout=15,
        )
    except (subprocess.TimeoutExpired, OSError):
        status.ssh_error = True
        status.overall_status = "ssh_error"
        return status

    if result.returncode != 0 and not result.stdout.strip():
        status.ssh_error = True
        status.overall_status = "ssh_error"
        return status

    # Parse structured output
    log_lines: list[str] = []
    in_log_block = False

    for line in result.stdout.splitlines():
        if line.startswith("SETUP:"):
            status.setup_complete = line.split(":", 1)[1].strip() == "yes"
        elif line.startswith("RUNNING:"):
            status.pipeline_running = line.split(":", 1)[1].strip() == "yes"
        elif line.startswith("TIME:"):
            try:
                epoch = int(line.split(":", 1)[1].strip())
                status.remote_now = _utc_from_epoch(epoch)
            except (ValueError, OSError):
                status.remote_now = datetime.now()
        elif line.startswith("STATE_JSON:"):
            json_str = line.split(":", 1)[1].strip()
            if json_str != "null":
                try:
                    status.state_json = json.loads(json_str)
                except json.JSONDecodeError:
                    pass
        elif line.strip() == "LOG_START":
            in_log_block = True
        elif line.strip() == "LOG_END":
            in_log_block = False
        elif in_log_block:
            log_lines.append(line)

    if status.remote_now is None:
        status.remote_now = datetime.now()

    # Early exit: still setting up
    if not status.setup_complete:
        status.overall_status = "setting_up"
        return status

    # No log lines: pipeline not started yet
    if not log_lines:
        status.overall_status = "not_started"
        return status

    # Parse log lines into phase history
    phases, started_at = parse_log_lines(log_lines)
    status.phase_history = phases
    status.started_at = started_at

    # Infer hardening rounds from state JSON or log
    if status.state_json and "pipeline_args" in status.state_json:
        pa = status.state_json["pipeline_args"]
        status.hardening_rounds = pa.get("hardening_rounds", 3)
    elif phases["phase_4"].max_rounds > 0:
        status.hardening_rounds = phases["phase_4"].max_rounds

    # Determine overall status
    pipeline_complete = any("Pipeline complete" in l for l in log_lines)
    has_failure = any(phases[k].status == "failed" for k in PHASE_ORDER)

    if pipeline_complete:
        status.overall_status = "complete"
    elif has_failure:
        status.overall_status = "failed"
    elif status.pipeline_running:
        status.overall_status = "running"
    else:
        status.overall_status = "stopped"

    return status


def poll_all(
    instances: list[InstanceInfo], ssh_key_path: str,
) -> list[InstanceStatus]:
    """Poll all instances in parallel via SSH."""
    results: list[InstanceStatus] = []
    max_workers = min(len(instances), 16) if instances else 1

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = {
            executor.submit(poll_instance, inst, ssh_key_path): inst
            for inst in instances
        }
        for future in as_completed(futures):
            try:
                results.append(future.result())
            except Exception:
                inst = futures[future]
                results.append(InstanceStatus(
                    env_id=inst.env_id,
                    instance_id=inst.instance_id,
                    ip=inst.ip,
                    ssh_error=True,
                    overall_status="ssh_error",
                ))

    # Sort: running (least-progressed first) > failed/stopped > setting up > complete
    def sort_key(s: InstanceStatus) -> tuple[int, float, str]:
        base = STATUS_SORT.get(s.overall_status, 5)
        progress = 0.0
        if s.overall_status == "running" and s.phase_history:
            completed, total, _ = compute_progress(
                s.phase_history, s.hardening_rounds,
            )
            progress = completed / total if total > 0 else 0.0
        return (base, progress, s.env_id)

    results.sort(key=sort_key)
    return results


# ---------------------------------------------------------------------------
# Rendering
# ---------------------------------------------------------------------------

def build_env_card(inst: InstanceStatus) -> Panel:
    """Render an expanded card for one environment."""
    text = Text()
    hr = inst.hardening_rounds
    total_steps = 5 + hr + 1

    # --- Special-case cards ---
    if inst.overall_status == "setting_up":
        text.append("  ")
        text.append("\u2591" * 35, style="dim")
        text.append(f" (0/{total_steps})\n", style="dim")
        text.append("  Waiting for instance setup to complete...\n", style="dim italic")
        return Panel(
            text,
            title=f" {inst.env_id} ",
            title_align="left",
            subtitle=" Setting up ",
            subtitle_align="right",
            border_style="dim",
        )

    if inst.overall_status == "ssh_error":
        text.append("  SSH connection failed\n", style="red")
        return Panel(
            text,
            title=f" {inst.env_id} ",
            title_align="left",
            subtitle=" SSH error ",
            subtitle_align="right",
            border_style="dim red",
        )

    if inst.overall_status == "not_started":
        text.append("  ")
        text.append("\u2591" * 35, style="dim")
        text.append(f" (0/{total_steps})\n", style="dim")
        text.append("  Pipeline not started yet\n", style="dim italic")
        return Panel(
            text,
            title=f" {inst.env_id} ",
            title_align="left",
            subtitle=" Not started ",
            subtitle_align="right",
            border_style="dim",
        )

    # --- Normal card with phase details ---
    phases = inst.phase_history
    completed, total, current_label = compute_progress(phases, hr)

    # Progress bar
    bar_width = 35
    filled = min(int(bar_width * completed / total), bar_width) if total > 0 else 0
    empty = bar_width - filled
    bar_style = "green" if completed >= total else "cyan"
    text.append("  ")
    text.append("\u2588" * filled, style=bar_style)
    text.append("\u2591" * empty, style="dim")
    text.append(f" {current_label} ({completed}/{total})\n")
    text.append("\n")

    # Per-phase lines
    for key in PHASE_ORDER:
        ph = phases.get(key, PhaseHistory())
        label, name = PHASE_DISPLAY[key]
        symbol, color = INDICATORS.get(ph.status, ("?", "dim"))
        is_active = ph.status == "running"

        # Main phase line
        text.append(f"  {label}  {name:<22s}", style="bold" if is_active else None)
        text.append(f" {symbol}", style=color)

        # Inline detail
        if key == "phase_2b":
            if ph.iterations and ph.status == "running":
                text.append(
                    f"  iter {ph.current_iter}/{ph.max_iter}", style="yellow",
                )
            elif ph.iterations and ph.status == "complete":
                text.append(f"  {len(ph.iterations)} iterations")
        elif key == "phase_3b":
            if ph.iterations and ph.status == "running":
                text.append(
                    f"  iter {ph.current_iter}/{ph.max_iter}", style="yellow",
                )
            elif ph.iterations and ph.status == "complete":
                text.append(f"  {len(ph.iterations)} iterations")
        elif key == "phase_4":
            if ph.status == "running" and ph.current_round > 0:
                text.append(
                    f"  round {ph.current_round}/{ph.max_rounds}",
                    style="yellow",
                )
            elif ph.status == "complete" and ph.rounds:
                text.append(f"  {len([r for r in ph.rounds if r])} rounds")

        text.append("\n")

        # Sub-detail lines (pass rate history)
        if key in ("phase_2b", "phase_3b") and ph.iterations:
            rates = " \u2192 ".join(
                f"{it['pass_rate']:.1f}%" for it in ph.iterations
            )
            text.append(f"           {rates}\n", style="dim")
        elif key == "phase_4" and ph.rounds:
            parts = [
                f"R{r['round']}: {r['pass_rate']:.1f}%"
                for r in ph.rounds if r
            ]
            if parts:
                text.append(f"           {'  '.join(parts)}\n", style="dim")
        elif key == "phase_5" and ph.status in ("complete", "running"):
            parts = []
            if ph.final_fn_rate is not None:
                parts.append(f"Fn: {ph.final_fn_rate:.1f}%")
            if ph.final_real_rate is not None:
                parts.append(f"Real: {ph.final_real_rate:.1f}%")
            if parts:
                text.append(
                    f"           {'  '.join(parts)}\n", style="dim",
                )

    # Border color + subtitle
    if inst.overall_status == "complete":
        border_style = "green"
        status_display = "Complete"
    elif inst.overall_status == "running":
        border_style = "yellow"
        status_display = "Running"
    elif inst.overall_status == "failed":
        border_style = "red"
        status_display = "Failed"
    elif inst.overall_status == "stopped":
        border_style = "red"
        status_display = "Stopped"
    else:
        border_style = "dim"
        status_display = inst.overall_status.replace("_", " ").title()

    elapsed = format_elapsed(inst.started_at, inst.remote_now)
    subtitle_parts = [status_display]
    if elapsed:
        subtitle_parts.append(elapsed)

    return Panel(
        text,
        title=f" {inst.env_id} ",
        title_align="left",
        subtitle=f" {' \u2014 '.join(subtitle_parts)} ",
        subtitle_align="right",
        border_style=border_style,
    )


def build_header(
    statuses: list[InstanceStatus],
    config: dict[str, str],
    countdown: int | None = None,
) -> Panel:
    """Build the summary header panel."""
    model = config.get("MODEL", "?")
    workers = config.get("WORKERS", "?")
    reps = config.get("REPETITIONS", "?")
    max_iter = config.get("MAX_ITERATIONS", "?")

    counts: dict[str, int] = {}
    for s in statuses:
        counts[s.overall_status] = counts.get(s.overall_status, 0) + 1

    summary_parts = [f"{len(statuses)} total"]
    for key, label in [
        ("running", "running"),
        ("complete", "complete"),
        ("failed", "failed"),
        ("stopped", "stopped"),
        ("setting_up", "setting up"),
        ("not_started", "not started"),
        ("ssh_error", "SSH error"),
    ]:
        if counts.get(key, 0) > 0:
            summary_parts.append(f"{counts[key]} {label}")

    now_str = datetime.now().strftime("%H:%M:%S")
    refresh_info = f"Last refresh: {now_str}"
    if countdown is not None:
        refresh_info += f"   Next in {countdown}s"

    text = Text()
    text.append(
        f"  Model: {model}   Workers: {workers}"
        f"   Repetitions: {reps}   Max Iterations: {max_iter}\n",
    )
    text.append(f"  Environments: {' \u2014 '.join(summary_parts)}\n")
    text.append(f"  {refresh_info}")

    return Panel(
        text,
        title=" Mirror-Mirror Pipeline Dashboard ",
        title_align="center",
        border_style="bright_blue",
    )


def build_dashboard(
    statuses: list[InstanceStatus],
    config: dict[str, str],
    countdown: int | None = None,
) -> Group:
    """Assemble the complete dashboard: header + all environment cards."""
    renderables = [build_header(statuses, config, countdown)]
    for s in statuses:
        renderables.append(build_env_card(s))
    return Group(*renderables)


# ---------------------------------------------------------------------------
# Log tail mode
# ---------------------------------------------------------------------------

def show_log(
    env_id: str,
    instances: list[InstanceInfo],
    ssh_key_path: str,
    n: int = 50,
) -> None:
    """Tail pipeline log for one environment and print to stdout."""
    inst = next((i for i in instances if i.env_id == env_id), None)
    if not inst:
        available = ", ".join(i.env_id for i in instances)
        print(f"ERROR: Unknown environment '{env_id}'")
        print(f"Available: {available}")
        sys.exit(1)

    cmd = [
        "ssh",
        "-i", ssh_key_path,
        "-o", "StrictHostKeyChecking=no",
        "-o", "ConnectTimeout=10",
        "-o", "BatchMode=yes",
        f"ec2-user@{inst.ip}",
        f"tail -n {n} /tmp/mirror-mirror-logs/pipeline.log 2>/dev/null"
        " || echo 'No log file found'",
    ]

    try:
        result = subprocess.run(
            cmd, capture_output=True, text=True, timeout=15,
        )
        if result.stdout:
            print(result.stdout, end="")
        if result.returncode != 0 and result.stderr:
            print(f"SSH error: {result.stderr.strip()}", file=sys.stderr)
    except subprocess.TimeoutExpired:
        print("ERROR: SSH connection timed out", file=sys.stderr)
        sys.exit(1)


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main() -> None:
    parser = argparse.ArgumentParser(
        description="Rich terminal dashboard for Mirror-Mirror pipeline monitoring",
    )
    parser.add_argument(
        "--interval", type=int, default=30,
        help="Refresh interval in seconds (default: 30)",
    )
    parser.add_argument(
        "--once", action="store_true",
        help="Print a single snapshot and exit",
    )
    parser.add_argument(
        "--log", metavar="ENV_ID",
        help="Tail pipeline log for the given environment",
    )
    parser.add_argument(
        "--log-lines", type=int, default=50,
        help="Number of log lines to show with --log (default: 50)",
    )
    parser.add_argument(
        "--launch-env", default="/tmp/mirror-mirror-launch.env",
        help="Path to launch.env file (default: /tmp/mirror-mirror-launch.env)",
    )
    args = parser.parse_args()

    # Load launch env
    try:
        config, instances = parse_launch_env(args.launch_env)
    except FileNotFoundError:
        print(f"ERROR: Launch file not found: {args.launch_env}")
        print("Run launch.sh first, or specify --launch-env PATH.")
        sys.exit(1)

    if not instances:
        print("ERROR: No instances found in launch file.")
        sys.exit(1)

    # Resolve SSH key path
    key_pair = config.get("KEY_PAIR", "")
    if not key_pair:
        print("ERROR: KEY_PAIR not found in launch file.")
        sys.exit(1)
    ssh_key_path = str(Path.home() / ".ssh" / f"{key_pair}.pem")

    # --log mode
    if args.log:
        show_log(args.log, instances, ssh_key_path, args.log_lines)
        return

    console = Console()

    # --once mode
    if args.once:
        console.print("[dim]Polling instances...[/dim]")
        statuses = poll_all(instances, ssh_key_path)
        dashboard = build_dashboard(statuses, config)
        console.clear()
        console.print(dashboard)
        return

    # Live dashboard — clear-and-print loop so tall output scrolls naturally
    try:
        while True:
            statuses = poll_all(instances, ssh_key_path)
            dashboard = build_dashboard(statuses, config)
            console.clear()
            console.print(dashboard)
            console.print(
                f"\n  [dim]Refreshing in {args.interval}s (Ctrl+C to stop)[/dim]",
            )
            time.sleep(args.interval)
    except KeyboardInterrupt:
        console.print("\n[dim]Dashboard stopped.[/dim]")


if __name__ == "__main__":
    main()
