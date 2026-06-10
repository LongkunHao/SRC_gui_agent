#!/usr/bin/env python3
"""Visualize Speculative Rollback Correction trajectories.

For each task in a rollout run dir, produce a self-contained HTML with:
  - one block per speculative branch (every attempt, NOT overwritten),
  - red dots for student click coordinates, purple dots for teacher
    corrections,
  - the model's raw textual response under each screenshot,
  - rollback verification: side-by-side "expected" (snapshot) vs
    "actual" (re-captured after rollback) screenshots,
  - click any image to open a lightbox at full resolution.

Usage:
    python src/viz_rollout.py <run_dir>
"""
from __future__ import annotations

import argparse
import base64
import html
import json
import struct
import sys
from pathlib import Path

VW, VH = 1920, 1080
QSCALE = 999


def png_size(p: Path) -> tuple[int, int]:
    try:
        with open(p, "rb") as f:
            f.seek(16)
            w, h = struct.unpack(">II", f.read(8))
        return w, h
    except Exception:
        return VW, VH


def img_data_uri(p: Path) -> str:
    if not p.is_file():
        return ""
    return "data:image/png;base64," + base64.b64encode(p.read_bytes()).decode()


def action_label(a: dict) -> str:
    t = a.get("type", "?")
    if t == "click":
        return f"click ({a.get('x')},{a.get('y')})"
    if t in ("type", "input"):
        txt = (a.get("text") or "")[:60]
        return f"type {txt!r}"
    if t == "key":
        return f"key {a.get('keys') or a.get('text')}"
    if t == "scroll":
        d = a.get("direction")
        amt = a.get("amount")
        bits = []
        if d:
            bits.append(d)
        if amt is not None:
            bits.append(f"amount={amt}")
        return "scroll " + " ".join(bits) if bits else "scroll"
    if t == "terminate":
        return f"terminate({a.get('status', '')})"
    if t in ("hover", "move"):
        return f"{t} ({a.get('x')},{a.get('y')})"
    return t


def action_dot(a: dict) -> tuple[int, int] | None:
    if a.get("type") in ("click", "hover", "move"):
        if "x" in a and "y" in a:
            return int(a["x"]), int(a["y"])
    return None


def teacher_dot(corr: dict) -> tuple[int, int] | None:
    if not corr:
        return None
    coord = corr.get("coordinate")
    if not coord or len(coord) < 2:
        return None
    try:
        x, y = float(coord[0]), float(coord[1])
    except (TypeError, ValueError):
        return None
    return int(x * VW / QSCALE), int(y * VH / QSCALE)


CSS = """
<style>
:root {
  --bg:#0e1117; --fg:#e6edf3; --muted:#8b949e; --accent:#58a6ff;
  --ok:#3fb950; --bad:#f85149; --warn:#d29922; --teach:#a371f7;
  --border:#30363d; --panel:#161b22; --panel2:#1c2128;
}
body { margin:0; padding:24px; background:var(--bg); color:var(--fg);
       font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
       font-size:14px; line-height:1.5; }
h1 { font-size:20px; margin:0 0 4px 0; }
h2 { font-size:16px; margin:24px 0 8px 0; color:var(--accent); }
.task-meta { color:var(--muted); margin-bottom:16px; }
.pill { display:inline-block; padding:2px 8px; border-radius:10px;
        font-size:12px; font-weight:600; margin-right:6px; }
.pill.pass { background:rgba(63,185,80,.15); color:var(--ok); border:1px solid var(--ok); }
.pill.fail { background:rgba(248,81,73,.15); color:var(--bad); border:1px solid var(--bad); }
.pill.int  { background:rgba(163,113,247,.15); color:var(--teach); border:1px solid var(--teach); }
.pill.k    { background:rgba(88,166,255,.15); color:var(--accent); border:1px solid var(--accent); }
.pill.warn { background:rgba(210,153,34,.15); color:var(--warn); border:1px solid var(--warn); }
.instruction { background:var(--panel); padding:12px 14px; border-left:3px solid var(--accent);
               border-radius:4px; margin-bottom:24px; }
.block { background:var(--panel); border:1px solid var(--border); border-radius:8px;
         padding:14px; margin-bottom:18px; }
.block.rejected { border-left:4px solid var(--bad); }
.block.accepted { border-left:4px solid var(--ok); }
.block.correction { border-left:4px solid var(--teach); background:var(--panel2); }
.block.verify    { border-left:4px solid var(--warn); background:var(--panel2); }
.block-header { display:flex; align-items:center; gap:8px; margin-bottom:10px; flex-wrap:wrap; }
.block-title { font-weight:600; font-size:15px; }
.reason { color:var(--muted); font-style:italic; margin:6px 0 10px 0; max-width:1100px; }
.steps { display:flex; gap:10px; flex-wrap:wrap; align-items:flex-start; }
.step  { width:340px; background:var(--bg); border:1px solid var(--border);
         border-radius:6px; overflow:hidden; display:flex; flex-direction:column; }
.step.discarded { opacity:.55; border-style:dashed; }
.step .imgwrap { position:relative; width:100%; cursor:zoom-in; }
.step .imgwrap img { width:100%; display:block; }
.step .dot { position:absolute; width:14px; height:14px; border-radius:50%;
             border:2px solid #fff; transform:translate(-50%, -50%);
             box-shadow:0 0 8px rgba(0,0,0,.7); pointer-events:none; }
.step .dot.student { background:var(--bad); }
.step .dot.teacher { background:var(--teach); }
.step .dot::after  { content:""; position:absolute; left:50%; top:50%;
                     width:34px; height:34px; border-radius:50%;
                     transform:translate(-50%,-50%);
                     border:2px solid currentColor; opacity:.55; }
.step .scroll-arrow {
    position:absolute; transform:translateX(-50%);
    color:var(--warn); font-size:64px; line-height:1;
    text-shadow:0 0 8px rgba(0,0,0,.9), 0 0 4px rgba(0,0,0,.9);
    pointer-events:none; font-weight:900;
}
.step .meta { padding:6px 8px; font-size:12px; }
.step .meta .idx { color:var(--accent); font-weight:600; margin-right:6px; }
.step .meta .act { font-family: ui-monospace, "JetBrains Mono", monospace;
                   font-size:11px; color:var(--fg); word-break:break-all; }
.step .meta .strike { text-decoration:line-through; color:var(--muted); }
.step .thought { font-size:11px; color:#c9d1d9; max-height:140px; overflow:auto;
                 border-top:1px dashed var(--border); padding:6px 8px;
                 font-family: ui-monospace, "JetBrains Mono", monospace;
                 white-space:pre-wrap; background:var(--panel2); }
.legend { color:var(--muted); font-size:12px; margin-bottom:16px; }
.legend .swatch { display:inline-block; width:10px; height:10px; border-radius:50%;
                  vertical-align:middle; margin:0 4px 0 8px; }
.legend .s { background:var(--bad);  } .legend .t { background:var(--teach); }
.tree { margin:18px 0 24px 0; padding-left:0; }
.tree ul { margin:8px 0 0 26px; padding-left:18px; border-left:1px solid var(--border); }
.tree li { list-style:none; margin:8px 0; }
.trunk-tree { margin:18px 0 24px 0; display:flex; flex-direction:column; gap:14px; }
.trunk { background:var(--panel); border:1px solid var(--border); border-radius:8px;
         padding:12px; }
.trunk.nested { margin-top:8px; background:var(--panel2); }
.trunk-head { display:flex; gap:8px; align-items:center; flex-wrap:wrap; margin-bottom:10px; }
.mainline { list-style:none; margin:0; padding:0 0 0 34px; position:relative; }
.mainline::before { content:""; position:absolute; left:12px; top:8px; bottom:8px;
                    border-left:2px solid var(--teach); }
.main-node { position:relative; margin:0 0 12px 0; }
.main-node::before { content:""; position:absolute; left:-28px; top:13px;
                     width:14px; height:14px; border-radius:50%;
                     background:var(--accent); border:2px solid var(--bg); }
.main-node.accepted::before { background:var(--ok); }
.main-node.rejected::before { background:var(--bad); }
.main-node.corrected::before { background:var(--teach); }
.node-card { display:inline-flex; gap:8px; align-items:center; flex-wrap:wrap;
             background:var(--panel2); border:1px solid var(--border);
             border-radius:6px; padding:8px 10px; }
.node-reason { color:var(--muted); font-size:12px; margin:4px 0 0 0;
               max-width:1100px; }
.offshoots { margin:8px 0 0 18px; padding-left:18px;
             border-left:1px dashed var(--border); }
.offshoot { margin:8px 0; }
.offshoot-label { color:var(--muted); font-size:12px; margin-bottom:4px; }
.leaf-node { display:inline-flex; gap:8px; align-items:center; flex-wrap:wrap;
             background:var(--panel); border:1px solid var(--border);
             border-radius:6px; padding:8px 10px; }
.leaf-node.side { background:rgba(248,81,73,.08); border-color:rgba(248,81,73,.45); }
.leaf-title { font-family:ui-monospace, "JetBrains Mono", monospace; font-weight:700; }
.leaf-section { border-top:1px solid var(--border); padding-top:18px; margin-top:22px; }
.leaf-grid { display:grid; grid-template-columns:repeat(auto-fit,minmax(260px,1fr));
             gap:10px; margin:12px 0 20px 0; }
.leaf-card { background:var(--panel); border:1px solid var(--border); border-radius:6px;
             padding:10px; }
.leaf-card .small { color:var(--muted); font-size:12px; }
a, a:visited { color:var(--accent); }
.toplinks { margin-bottom:16px; }
table.summary { border-collapse:collapse; width:100%; margin-bottom:24px; }
table.summary th, table.summary td { padding:6px 10px; border-bottom:1px solid var(--border);
                                     text-align:left; }
table.summary th { color:var(--muted); font-weight:500; font-size:12px; }
table.summary tr:hover { background:var(--panel); }

#lightbox { position:fixed; inset:0; background:rgba(0,0,0,0.92); display:none;
            z-index:9999; cursor:zoom-out; }
#lightbox.open { display:flex; align-items:center; justify-content:center; }
#lightbox img { max-width:98vw; max-height:98vh; box-shadow:0 0 40px rgba(0,0,0,0.8); }
#lightbox .close { position:absolute; top:14px; right:20px; color:#fff;
                   font-size:30px; cursor:pointer; user-select:none; }
</style>
<script>
function openLB(ev, src) {
  const lb = document.getElementById('lightbox');
  document.getElementById('lightbox-img').src = src;
  lb.classList.add('open');
  ev.stopPropagation();
}
function closeLB() {
  document.getElementById('lightbox').classList.remove('open');
}
document.addEventListener('keydown', e => { if (e.key === 'Escape') closeLB(); });
</script>
"""


def _img_card(*, img_uri, img_w, img_h, idx_label, action_text,
              dot=None, dot_kind="student", discarded=False, thought=None,
              scroll=None):
    """Render one image card with optional click-dot or scroll arrow overlay.

    ``scroll`` is an optional dict with keys {direction: 'up'|'down',
    amount: int|None}; when present we draw a vertical arrow through
    image center indicating scroll direction & magnitude.
    """
    cls = "step discarded" if discarded else "step"
    dot_html = ""
    if dot is not None and img_w and img_h:
        x_pct = 100.0 * dot[0] / img_w
        y_pct = 100.0 * dot[1] / img_h
        dot_html = (f'<div class="dot {dot_kind}" '
                    f'style="left:{x_pct:.2f}%;top:{y_pct:.2f}%;"></div>')
    arrow_html = ""
    if scroll is not None:
        # Arrow length proportional to amount, capped to viewport half.
        amt = scroll.get("amount") or 0
        d = scroll.get("direction") or "down"
        try:
            mag = min(45.0, max(8.0, float(int(amt)) * 5.0))  # in % of height
        except Exception:
            mag = 20.0
        # Center the arrow horizontally; start at middle, extend in dir.
        if d == "down":
            arrow_html = (
                f'<div class="scroll-arrow" style="left:50%;top:50%;'
                f'height:{mag:.1f}%;">&darr;</div>'
            )
        else:
            arrow_html = (
                f'<div class="scroll-arrow" style="left:50%;'
                f'top:{50 - mag:.1f}%;height:{mag:.1f}%;">&uarr;</div>'
            )
    label_html = html.escape(action_text)
    if discarded:
        label_html = f'<span class="strike">{label_html}</span>'
    thought_html = ""
    if thought:
        thought_html = f'<div class="thought">{html.escape(thought)}</div>'
    return (
        f'<div class="{cls}">'
        f'  <div class="imgwrap" onclick="openLB(event, this.querySelector(\'img\').src)">'
        f'    <img src="{img_uri}" />'
        f'    {dot_html}'
        f'    {arrow_html}'
        f'  </div>'
        f'  <div class="meta"><span class="idx">{html.escape(idx_label)}</span>'
        f'  <span class="act">{label_html}</span></div>'
        f'  {thought_html}'
        f'</div>'
    )


def _first_png_size(ss_dir: Path, branches: list[dict]) -> tuple[int, int]:
    for br in branches:
        for key in ("step_imgs",):
            for name in br.get(key) or []:
                p = ss_dir / name
                if p.is_file():
                    return png_size(p)
        for key in ("post_img", "corr_img", "rb_verify_img"):
            name = br.get(key)
            if name and (ss_dir / name).is_file():
                return png_size(ss_dir / name)
    for p in ss_dir.rglob("*.png"):
        return png_size(p)
    return VW, VH


def _append_branch_cards(parts: list[str], *, branches: list[dict],
                         actions: list[list[dict]], get_img,
                         img_w: int, img_h: int, label_prefix: str = "") -> None:
    for bi, br in enumerate(branches, 1):
        accepted = br.get("accepted")
        rb = br.get("rollback_to")
        bl = br.get("branch_len", 0)
        kept = (bl if accepted else max(0, min(rb or 0, bl)))
        cls = "block accepted" if accepted else "block rejected"
        label = ("ACCEPTED" if accepted else f"REJECTED -> rollback to step {rb}")
        color_pill = ("pill pass" if accepted else "pill fail")
        branch_label = f"{label_prefix}Branch #{bi}" if label_prefix else f"Branch #{bi}"

        parts.append(f'<div class="{cls}">')
        parts.append('<div class="block-header">'
                     f'<span class="block-title">{html.escape(branch_label)}</span>'
                     f'<span class="{color_pill}">{html.escape(label)}</span>'
                     f'<span class="pill k">start={br.get("branch_start")}</span>'
                     f'<span class="pill k">len={bl}</span>'
                     '</div>')
        if br.get("reason"):
            parts.append(f'<div class="reason">"{html.escape(br["reason"])}"</div>')

        parts.append('<div class="steps">')
        thoughts = br.get("thoughts") or []
        step_imgs = br.get("step_imgs") or []
        br_actions = br.get("actions")
        bs = br.get("branch_start", 0)
        for j, img_name in enumerate(step_imgs):
            abs_idx = bs + j
            a = {}
            if br_actions and j < len(br_actions) and br_actions[j]:
                a = br_actions[j][0]
            elif abs_idx < len(actions) and actions[abs_idx]:
                a = actions[abs_idx][0]
            discarded = (not accepted) and (j >= kept)
            scroll_info = None
            if a.get("type") == "scroll":
                scroll_info = {"direction": a.get("direction"),
                               "amount": a.get("amount")}
            parts.append(_img_card(
                img_uri=get_img(img_name),
                img_w=img_w, img_h=img_h,
                idx_label=f"s{j} abs={abs_idx}",
                action_text=action_label(a) if a else "(no action)",
                dot=action_dot(a),
                dot_kind="student",
                discarded=discarded,
                thought=thoughts[j] if j < len(thoughts) else None,
                scroll=scroll_info,
            ))
        if br.get("post_img"):
            parts.append(_img_card(
                img_uri=get_img(br["post_img"]),
                img_w=img_w, img_h=img_h,
                idx_label="post",
                action_text="teacher review screenshot",
            ))
        parts.append('</div></div>')

        if not accepted and br.get("rb_verify_img"):
            parts.append('<div class="block verify">')
            parts.append('<div class="block-header">'
                         '<span class="block-title">Rollback verify</span>'
                         f'<span class="pill warn">restored abs {bs + kept}</span>'
                         '</div><div class="steps">')
            if br.get("rb_expected_img"):
                parts.append(_img_card(
                    img_uri=get_img(br["rb_expected_img"]),
                    img_w=img_w, img_h=img_h,
                    idx_label="expected",
                    action_text="snapshot at rollback target",
                ))
            parts.append(_img_card(
                img_uri=get_img(br["rb_verify_img"]),
                img_w=img_w, img_h=img_h,
                idx_label="actual",
                action_text="after reset+replay",
            ))
            parts.append('</div></div>')

        if not accepted and br.get("correction") and br.get("corr_img"):
            corr_raw = br["correction"]
            corrs = corr_raw if isinstance(corr_raw, list) else [corr_raw]
            corrs = [c for c in corrs if isinstance(c, dict)]
            if corrs:
                parts.append('<div class="block correction">')
                parts.append('<div class="block-header">'
                             '<span class="block-title">Teacher correction</span>'
                             f'<span class="pill int">{len(corrs)} action(s)</span>'
                             '</div>')
                raw = br.get("correction_raw") or ""
                if raw:
                    parts.append(
                        '<details class="reason" style="white-space:pre-wrap;'
                        'font-family:ui-monospace,monospace;font-size:11px;'
                        'max-width:1200px;">'
                        '<summary>teacher raw response</summary>'
                        f'{html.escape(raw)}</details>'
                    )
                parts.append('<div class="steps">')
                for ci, corr in enumerate(corrs):
                    dot = teacher_dot(corr)
                    parts.append(_img_card(
                        img_uri=get_img(br["corr_img"]),
                        img_w=img_w, img_h=img_h,
                        idx_label=f"correction.{ci}",
                        action_text=(f"{corr.get('action','?')} "
                                     f"coord={corr.get('coordinate')} "
                                     f"text={(corr.get('text') or '')[:40]!r}"),
                        dot=dot,
                        dot_kind="teacher",
                    ))
                parts.append('</div></div>')


def render_branching_task_html(task_dir: Path, out_path: Path,
                               instruction: str, result: dict,
                               meta: dict) -> None:
    ss_dir = task_dir / "screenshots"
    leaves_dir = task_dir / "leaves"
    img_cache: dict[str, str] = {}

    def get_img(name):
        if not name:
            return ""
        if name not in img_cache:
            img_cache[name] = img_data_uri(ss_dir / name)
        return img_cache[name]

    leaf_results = result.get("leaves") or []
    leaf_details: dict[str, dict] = {}
    all_branches: list[dict] = []
    for lr in leaf_results:
        lid = lr.get("leaf_id")
        detail = {}
        if lid and (leaves_dir / f"{lid}.json").is_file():
            try:
                detail = json.loads((leaves_dir / f"{lid}.json").read_text())
            except Exception:
                detail = {}
        if lid:
            leaf_details[lid] = {**lr, **detail}
            all_branches.extend(detail.get("branches") or [])
    if not all_branches:
        all_branches = meta.get("branches") or []

    img_w, img_h = _first_png_size(ss_dir, all_branches)
    passed = result.get("passed", False)
    pass_pill = ('<span class="pill pass">PASS</span>' if passed
                 else '<span class="pill fail">FAIL</span>')
    parts = ["<!DOCTYPE html><html><head><meta charset='utf-8'>"
             f"<title>{html.escape(task_dir.name)}</title>", CSS,
             "</head><body>"]
    parts.append('<div class="toplinks"><a href="index.html">&larr; index</a></div>')
    parts.append(f"<h1>{html.escape(task_dir.name)}</h1>")
    parts.append('<div class="task-meta">')
    parts.append(pass_pill)
    parts.append(f'<span class="pill k">K={meta.get("K", 0)}</span>')
    parts.append(f'<span class="pill k">{result.get("num_leaves", len(leaf_results))} leaves</span>')
    parts.append(f'<span class="pill pass">{result.get("num_passed_leaves", 0)} pass leaves</span>')
    parts.append(f'<span class="pill int">{result.get("forks_used", 0)} forks</span>')
    parts.append(f'<span class="pill k">{result.get("branch_workers", meta.get("branch_workers", 1))} workers</span>')
    parts.append(f' &middot; {result.get("elapsed", 0)}s')
    parts.append('</div>')
    parts.append(f'<div class="instruction"><b>Task:</b> {html.escape(instruction)}</div>')
    if result.get("verifier_message"):
        parts.append(f'<div class="reason"><b>Verifier:</b> {html.escape(str(result["verifier_message"]))}</div>')
    if result.get("errors"):
        parts.append('<div class="reason"><b>Errors:</b> ' +
                     html.escape("; ".join(str(e) for e in result["errors"]))[:800] +
                     '</div>')
    parts.append('<div class="legend">'
                 '<span class="swatch s"></span>student click '
                 '<span class="swatch t"></span>teacher correction '
                 '&middot; mainline is the teacher-corrected path; side leaves are rejected student branches '
                 '&middot; click any image to zoom'
                 '</div>')

    by_parent: dict[str | None, list[dict]] = {}
    for lr in leaf_results:
        by_parent.setdefault(lr.get("parent_id"), []).append(lr)
    for kids in by_parent.values():
        kids.sort(key=lambda r: r.get("leaf_id", ""))

    def _branch_no(br: dict | None, default=None):
        if not br:
            return default
        val = br.get("branch_no", default)
        if val is None:
            return default
        try:
            return int(val)
        except (TypeError, ValueError):
            return default

    def _leaf_detail(lr: dict) -> dict:
        lid = lr.get("leaf_id")
        return leaf_details.get(lid, lr) if lid else lr

    def _visible_branches(lr: dict, after_branch_no: int = 0) -> list[tuple[int, dict]]:
        detail = _leaf_detail(lr)
        rows: list[tuple[int, dict]] = []
        for idx, br in enumerate(detail.get("branches") or [], 1):
            bno = _branch_no(br, idx)
            if bno is None:
                continue
            if bno > after_branch_no:
                rows.append((bno, br))
        rows.sort(key=lambda item: item[0])
        return rows

    child_forks: dict[str, dict] = {}
    children_by_parent_branch: dict[tuple[str, int | None], list[dict]] = {}
    for lr in leaf_results:
        lid = lr.get("leaf_id")
        parent_id = lr.get("parent_id")
        if not lid or not parent_id:
            continue
        detail = _leaf_detail(lr)
        fork_rec: dict = {}
        for rec in detail.get("teacher_decisions") or []:
            if (
                rec.get("leaf_id") == lid
                and rec.get("parent_leaf_id") == parent_id
            ):
                fork_rec = rec
        if not fork_rec:
            for rec in detail.get("teacher_decisions") or []:
                if rec.get("leaf_id") == lid and rec.get("kept_for_exploration"):
                    fork_rec = rec
        child_forks[lid] = fork_rec
        fork_branch_no = _branch_no(fork_rec, None)
        children_by_parent_branch.setdefault(
            (parent_id, fork_branch_no), []
        ).append(lr)
    for kids in children_by_parent_branch.values():
        kids.sort(key=lambda r: r.get("leaf_id", ""))

    def leaf_badge(lr: dict) -> str:
        detail = _leaf_detail(lr)
        return ('<span class="pill pass">PASS</span>' if detail.get("passed")
                else '<span class="pill fail">FAIL</span>')

    def leaf_summary_node(lr: dict, *, side: bool = False) -> str:
        detail = _leaf_detail(lr)
        lid = detail.get("leaf_id", lr.get("leaf_id", "?"))
        role = html.escape(str(lr.get("role") or "leaf"))
        reason = html.escape(str(lr.get("fork_reason") or ""))[:120]
        extra = f'<span class="pill warn">{reason}</span>' if reason else ""
        side_cls = " side" if side else ""
        return (
            f'<div class="leaf-node{side_cls}">'
            f'<a class="leaf-title" href="#{html.escape(str(lid), quote=True)}">'
            f'{html.escape(str(lid))}</a>{leaf_badge(lr)}'
            f'<span class="pill k">{role}</span>'
            f'<span class="pill k">{detail.get("steps", 0)} steps</span>'
            f'<span class="pill int">{detail.get("teacher_interventions", 0)} int</span>'
            f'{extra}</div>'
        )

    def render_mainline(lr: dict, *, after_branch_no: int = 0,
                        nested: bool = False, seen: set[str] | None = None) -> str:
        detail = _leaf_detail(lr)
        lid = str(detail.get("leaf_id", lr.get("leaf_id", "?")))
        seen = set(seen or set())
        if lid in seen:
            return ""
        seen.add(lid)
        branches = _visible_branches(lr, after_branch_no)
        if nested and not branches:
            return ""

        html_parts: list[str] = [
            f'<div class="trunk{" nested" if nested else ""}">',
            '<div class="trunk-head">',
            leaf_summary_node(lr),
            '</div>',
        ]
        if branches:
            html_parts.append('<ol class="mainline">')
            for bno, br in branches:
                accepted = bool(br.get("accepted"))
                corrected = (not accepted) and bool(br.get("correction"))
                node_cls = "accepted" if accepted else "rejected"
                if corrected:
                    node_cls += " corrected"
                label = "ACCEPTED" if accepted else "REJECTED"
                pill_cls = "pill pass" if accepted else "pill fail"
                if corrected:
                    label = "REJECTED -> TEACHER CORRECTION"
                    pill_cls = "pill int"
                html_parts.append(f'<li class="main-node {node_cls}">')
                html_parts.append(
                    '<div class="node-card">'
                    f'<span class="block-title">Branch #{bno}</span>'
                    f'<span class="{pill_cls}">{html.escape(label)}</span>'
                    f'<span class="pill k">start={br.get("branch_start")}</span>'
                    f'<span class="pill k">len={br.get("branch_len", 0)}</span>'
                    '</div>'
                )
                if br.get("reason"):
                    reason = html.escape(str(br["reason"]))[:260]
                    html_parts.append(f'<div class="node-reason">{reason}</div>')

                offshoots = children_by_parent_branch.get((lid, bno), [])
                if offshoots:
                    html_parts.append('<div class="offshoots">')
                    for child in offshoots:
                        child_lid = str(child.get("leaf_id", "?"))
                        fork = child_forks.get(child_lid, {})
                        child_after = _branch_no(fork, bno) or bno
                        html_parts.append('<div class="offshoot">')
                        html_parts.append(
                            f'<div class="offshoot-label">student leaf forked '
                            f'from Branch #{bno}</div>'
                        )
                        html_parts.append(leaf_summary_node(child, side=True))
                        continuation = render_mainline(
                            child,
                            after_branch_no=child_after,
                            nested=True,
                            seen=seen,
                        )
                        if continuation:
                            html_parts.append(continuation)
                        html_parts.append('</div>')
                    html_parts.append('</div>')
                html_parts.append('</li>')
            html_parts.append('</ol>')
        else:
            html_parts.append('<div class="node-reason">No branch records for this leaf.</div>')

        loose_children = children_by_parent_branch.get((lid, None), [])
        if loose_children:
            html_parts.append('<div class="offshoots">')
            for child in loose_children:
                html_parts.append('<div class="offshoot">')
                html_parts.append('<div class="offshoot-label">student leaf forked from unknown branch</div>')
                html_parts.append(leaf_summary_node(child, side=True))
                html_parts.append('</div>')
            html_parts.append('</div>')
        html_parts.append('</div>')
        return "".join(html_parts)

    roots = by_parent.get(None) or [
        lr for lr in leaf_results if not lr.get("parent_id")
    ]
    parts.append('<h2>Teacher Mainline And Forks</h2><div class="trunk-tree">')
    parts.append("".join(render_mainline(r) for r in roots))
    parts.append('</div>')

    parts.append('<h2>Leaf Summary</h2><div class="leaf-grid">')
    for lr in leaf_results:
        lid = lr.get("leaf_id", "?")
        pill = ('<span class="pill pass">PASS</span>' if lr.get("passed")
                else '<span class="pill fail">FAIL</span>')
        msg = html.escape(str(lr.get("verifier_message", "")))[:180]
        parts.append(
            '<div class="leaf-card">'
            f'<div><span class="leaf-title">{html.escape(lid)}</span> {pill}</div>'
            f'<div class="small">role={html.escape(str(lr.get("role","")))}, '
            f'parent={html.escape(str(lr.get("parent_id") or ""))}, '
            f'steps={lr.get("steps",0)}, int={lr.get("teacher_interventions",0)}</div>'
            f'<div class="small">{msg}</div></div>'
        )
    parts.append('</div>')

    for lr in leaf_results:
        lid = lr.get("leaf_id")
        detail = leaf_details.get(lid, {})
        branches = detail.get("branches") or []
        actions = detail.get("actions_per_step") or []
        parts.append(f'<div class="leaf-section" id="{html.escape(str(lid))}">')
        parts.append(f'<h2>{html.escape(str(lid))}</h2>')
        if not branches:
            parts.append('<div class="reason">No branch records for this leaf.</div>')
        _append_branch_cards(
            parts,
            branches=branches,
            actions=actions,
            get_img=get_img,
            img_w=img_w,
            img_h=img_h,
            label_prefix=f"{lid} ",
        )
        parts.append('</div>')

    parts.append('<div id="lightbox" onclick="closeLB()">'
                 '<span class="close" onclick="closeLB()">&times;</span>'
                 '<img id="lightbox-img" /></div>')
    parts.append("</body></html>")
    out_path.write_text("".join(parts))


def render_task_html(task_dir: Path, out_path: Path,
                     instruction: str, result: dict) -> None:
    meta_path = task_dir / "rollout_meta.json"
    if not meta_path.is_file():
        return
    meta = json.loads(meta_path.read_text())
    if result.get("branching") or meta.get("algorithm") == "branching_src":
        render_branching_task_html(task_dir, out_path, instruction, result, meta)
        return
    actions = meta.get("actions_per_step", [])
    branches = meta.get("branches", [])
    interventions = meta.get("teacher_interventions", 0)
    K = meta.get("K", 0)

    ss_dir = task_dir / "screenshots"
    img_cache: dict[str, str] = {}

    def get_img(name):
        if not name:
            return ""
        if name not in img_cache:
            img_cache[name] = img_data_uri(ss_dir / name)
        return img_cache[name]

    img_w, img_h = png_size(ss_dir / "step_0.png")
    if not img_w:
        img_w, img_h = VW, VH

    passed = result.get("passed", False)
    pass_pill = ('<span class="pill pass">PASS</span>' if passed
                 else '<span class="pill fail">FAIL</span>')
    n_steps = result.get("steps", len(actions))
    elapsed = result.get("elapsed", 0)
    verdict_msg = result.get("verifier_message", "")
    err_list = result.get("errors") or []

    parts = ["<!DOCTYPE html><html><head><meta charset='utf-8'>"
             f"<title>{html.escape(task_dir.name)}</title>", CSS,
             "</head><body>"]
    parts.append('<div class="toplinks"><a href="index.html">&larr; index</a></div>')
    parts.append(f"<h1>{html.escape(task_dir.name)}</h1>")
    parts.append('<div class="task-meta">')
    parts.append(pass_pill)
    parts.append(f'<span class="pill k">K={K}</span>')
    parts.append(f'<span class="pill int">{interventions} interventions</span>')
    parts.append(f'<span class="pill k">{len(branches)} branches</span>')
    parts.append(f' &middot; {n_steps} steps &middot; {elapsed}s')
    parts.append('</div>')
    parts.append(f'<div class="instruction"><b>Task:</b> {html.escape(instruction)}</div>')
    if verdict_msg:
        parts.append(f'<div class="reason"><b>Verifier:</b> {html.escape(str(verdict_msg))}</div>')
    if err_list:
        parts.append('<div class="reason"><b>Errors:</b> ' +
                     html.escape("; ".join(str(e) for e in err_list))[:500] + '</div>')
    parts.append('<div class="legend">'
                 '<span class="swatch s"></span>student click '
                 '<span class="swatch t"></span>teacher correction '
                 '&middot; dashed/struck = rolled-back attempt '
                 '&middot; click any image to zoom'
                 '</div>')

    if not branches:
        parts.append('<div class="reason">No <code>branches</code> field '
                     'in rollout_meta.json (this run predates per-branch '
                     'logging — re-run to get full visualization).</div>')

    for bi, br in enumerate(branches, 1):
        accepted = br.get("accepted")
        rb = br.get("rollback_to")
        bl = br.get("branch_len", 0)
        kept = (bl if accepted else max(0, min(rb or 0, bl)))
        cls = "block accepted" if accepted else "block rejected"
        label = ("ACCEPTED" if accepted
                 else f"REJECTED → rollback to step {rb}")
        color_pill = ("pill pass" if accepted else "pill fail")
        parts.append(f'<div class="{cls}">')
        parts.append('<div class="block-header">'
                     f'<span class="block-title">Branch #{bi}</span>'
                     f'<span class="{color_pill}">{label}</span>'
                     f'<span class="pill k">branch_start={br.get("branch_start")}</span>'
                     f'<span class="pill k">len={bl}</span>'
                     '</div>')
        if br.get("reason"):
            parts.append(f'<div class="reason">"{html.escape(br["reason"])}"</div>')

        parts.append('<div class="steps">')
        thoughts = br.get("thoughts") or []
        step_imgs = br.get("step_imgs") or []
        # Prefer per-branch actions (captured BEFORE rollback overwrote
        # the surviving timeline). Fall back to actions_per_step for old
        # meta files that lack the per-branch field.
        br_actions = br.get("actions")
        bs = br.get("branch_start", 0)
        for j, img_name in enumerate(step_imgs):
            abs_idx = bs + j
            a = {}
            if br_actions and j < len(br_actions) and br_actions[j]:
                a = br_actions[j][0]
            elif abs_idx < len(actions) and actions[abs_idx]:
                a = actions[abs_idx][0]
            discarded = (not accepted) and (j >= kept)
            scroll_info = None
            if a.get("type") == "scroll":
                scroll_info = {"direction": a.get("direction"),
                               "amount": a.get("amount")}
            parts.append(_img_card(
                img_uri=get_img(img_name),
                img_w=img_w, img_h=img_h,
                idx_label=f"b{bi}.s{j}  (abs={abs_idx})",
                action_text=action_label(a) if a else "(no action)",
                dot=action_dot(a),
                dot_kind="student",
                discarded=discarded,
                thought=thoughts[j] if j < len(thoughts) else None,
                scroll=scroll_info,
            ))
        post = br.get("post_img")
        if post:
            parts.append(_img_card(
                img_uri=get_img(post), img_w=img_w, img_h=img_h,
                idx_label="post-branch",
                action_text=("snapshot AFTER all K student steps — this is "
                             "the image the teacher saw to decide accept/reject"),
            ))
        parts.append('</div></div>')

        # Rollback verification
        if not accepted and br.get("rb_verify_img"):
            parts.append('<div class="block verify">')
            parts.append('<div class="block-header">'
                         '<span class="block-title">Rollback verify</span>'
                         f'<span class="pill warn">restored to abs step '
                         f'{bs + kept}</span></div>')
            parts.append('<div class="reason">Compare expected (snapshot at '
                         'rollback target) vs actual (re-captured right '
                         'after rollback). They should match if rollback '
                         'succeeded.</div>')
            parts.append('<div class="steps">')
            exp = br.get("rb_expected_img")
            if exp:
                parts.append(_img_card(
                    img_uri=get_img(exp), img_w=img_w, img_h=img_h,
                    idx_label="expected", action_text="snapshot at rollback target",
                ))
            parts.append(_img_card(
                img_uri=get_img(br["rb_verify_img"]),
                img_w=img_w, img_h=img_h,
                idx_label="actual", action_text="re-captured after rollback",
            ))
            parts.append('</div></div>')

        # Teacher correction. ``correction`` is a list of computer_use
        # param dicts (one per <tool_call> the teacher emitted). Older runs
        # stored a single dict — normalize to a list for backwards compat.
        if not accepted and br.get("correction") and br.get("corr_img"):
            corr_raw = br["correction"]
            corrs = corr_raw if isinstance(corr_raw, list) else [corr_raw]
            corrs = [c for c in corrs if isinstance(c, dict)]
            if corrs:
                summary = " ; ".join(
                    f'{c.get("action","?")} coord={c.get("coordinate")}'
                    for c in corrs
                )
                parts.append('<div class="block correction">')
                parts.append('<div class="block-header">'
                             '<span class="block-title">Teacher correction</span>'
                             f'<span class="pill int">{html.escape(summary)}</span></div>')
                if br.get("reason"):
                    parts.append(f'<div class="reason">"{html.escape(br["reason"])}"</div>')
                # Surface the teacher's full second-shot response (thought
                # + raw <tool_call>) so we can debug why the correction was
                # what it was, mirroring the per-step ``thought`` panel
                # rendered for student steps.
                raw = br.get("correction_raw") or ""
                if raw:
                    parts.append(
                        '<details class="reason" style="white-space:pre-wrap;'
                        'font-family:ui-monospace,monospace;font-size:11px;'
                        'max-width:1200px;">'
                        '<summary>teacher raw response</summary>'
                        f'{html.escape(raw)}</details>'
                    )
                parts.append('<div class="steps">')
                # Render one card per teacher action; reuse the same
                # post-rollback screenshot for all cards (we only captured
                # one corr_img for the whole synthetic step).
                for ci, corr in enumerate(corrs):
                    dot = teacher_dot(corr)
                    corr_scroll = None
                    if corr.get("action") == "scroll":
                        try:
                            corr_amount = max(1, int(float(corr.get("amount", 3))))
                        except (ValueError, TypeError):
                            corr_amount = 3
                        corr_dir = str(corr.get("direction", "down")).lower()
                        if corr_dir not in ("up", "down", "left", "right"):
                            corr_dir = "down"
                        corr_scroll = {
                            "direction": corr_dir,
                            "amount": corr_amount,
                        }
                    label = "correction" if len(corrs) == 1 else f"correction.{ci}"
                    parts.append(_img_card(
                        img_uri=get_img(br["corr_img"]),
                        img_w=img_w, img_h=img_h,
                        idx_label=label,
                        action_text=(f"{corr.get('action','?')} "
                                     f"coord={corr.get('coordinate')} "
                                     f"text={(corr.get('text') or '')[:40]!r}"),
                        dot=dot, dot_kind="teacher",
                        scroll=corr_scroll,
                    ))
                parts.append('</div></div>')

    parts.append('<div id="lightbox" onclick="closeLB()">'
                 '<span class="close" onclick="closeLB()">&times;</span>'
                 '<img id="lightbox-img" /></div>')
    parts.append("</body></html>")
    out_path.write_text("".join(parts))


def render_index(run_dir: Path, viz_dir: Path,
                 task_summaries: list[dict]) -> None:
    parts = ["<!DOCTYPE html><html><head><meta charset='utf-8'>"
             "<title>Rollout viz index</title>", CSS, "</head><body>"]
    parts.append(f"<h1>Speculative Rollback Rollout — {html.escape(run_dir.name)}</h1>")
    n_pass = sum(1 for t in task_summaries if t["passed"])
    n_total = len(task_summaries)
    n_int = sum(t.get("interventions", 0) for t in task_summaries)
    parts.append(f'<div class="task-meta">'
                 f'<span class="pill pass">{n_pass}/{n_total} passed '
                 f'({100.0*n_pass/max(1,n_total):.1f}%)</span>'
                 f'<span class="pill int">{n_int} total interventions</span>'
                 f'</div>')
    parts.append('<table class="summary">'
                 '<tr><th>Task</th><th>Result</th><th>Steps</th>'
                 '<th>Interventions</th><th>Time (s)</th>'
                 '<th>Branches</th><th>Leaves</th><th>Instruction</th></tr>')
    for t in task_summaries:
        pill = ('<span class="pill pass">PASS</span>' if t["passed"]
                else '<span class="pill fail">FAIL</span>')
        link = f'<a href="{t["html"]}">{html.escape(t["task_id"])}</a>'
        parts.append(
            f'<tr><td>{link}</td><td>{pill}</td>'
            f'<td>{t.get("steps", "?")}</td>'
            f'<td>{t.get("interventions", 0)}</td>'
            f'<td>{t.get("elapsed", 0)}</td>'
            f'<td>{t.get("branches", 0)}</td>'
            f'<td>{t.get("pass_leaves", 0)}/{t.get("leaves", 1)}</td>'
            f'<td>{html.escape(t.get("instruction", ""))[:140]}</td></tr>'
        )
    parts.append('</table></body></html>')
    (viz_dir / "index.html").write_text("".join(parts))


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("run_dir")
    args = ap.parse_args()
    run_dir = Path(args.run_dir).resolve()
    if not run_dir.is_dir():
        print(f"Not a dir: {run_dir}", file=sys.stderr)
        sys.exit(1)
    viz_dir = run_dir / "viz"
    viz_dir.mkdir(exist_ok=True)

    instructions = {}
    agg = run_dir / "results.json"
    if agg.is_file():
        try:
            ag = json.loads(agg.read_text())
            for r in (ag.get("results") or []):
                instructions[r["task_id"]] = r.get("instruction", "")
        except Exception:
            pass

    summaries = []
    for sub in sorted(run_dir.iterdir()):
        if not sub.is_dir() or not sub.name.startswith("task_"):
            continue
        rj = sub / "result.json"
        if not rj.is_file():
            continue
        try:
            r = json.loads(rj.read_text())
        except Exception:
            continue
        instruction = instructions.get(r.get("task_id", sub.name),
                                        r.get("instruction", ""))
        out_html = viz_dir / f"{sub.name}.html"
        try:
            render_task_html(sub, out_html, instruction, r)
        except Exception as e:
            print(f"  ! failed to render {sub.name}: {e}", file=sys.stderr)
            continue
        meta_path = sub / "rollout_meta.json"
        ints, nbr = 0, 0
        if meta_path.is_file():
            try:
                m = json.loads(meta_path.read_text())
                ints = m.get("teacher_interventions_total",
                             m.get("teacher_interventions", 0))
                nbr = len(m.get("branches", m.get("teacher_decisions", [])))
            except Exception:
                pass
        summaries.append({
            "task_id": r.get("task_id", sub.name),
            "html": out_html.name,
            "passed": r.get("passed", False),
            "steps": r.get("steps", 0),
            "interventions": ints,
            "branches": nbr,
            "leaves": r.get("num_leaves", 1),
            "pass_leaves": r.get("num_passed_leaves", int(r.get("passed", False))),
            "elapsed": r.get("elapsed", 0),
            "instruction": instruction,
        })
        print(f"  ✓ {sub.name}")

    render_index(run_dir, viz_dir, summaries)
    print(f"\nWrote {len(summaries)} task htmls + index.html to {viz_dir}")


if __name__ == "__main__":
    main()
