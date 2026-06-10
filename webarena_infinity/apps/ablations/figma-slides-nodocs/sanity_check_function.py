#!/usr/bin/env python3
"""
Sanity check for Figma Slides function-test tasks.

For each task, directly applies the expected end-state (bypassing the agent),
then runs the verifier and asserts it passes.

Usage:
    python3 sanity_check_function.py                     # All tasks, sequential
    python3 sanity_check_function.py --workers N          # N parallel environments
    python3 sanity_check_function.py --task-id task_5     # Single task
    python3 sanity_check_function.py --port 9000          # Custom base port
"""
import argparse
import importlib.util
import json
import os
import socket
import subprocess
import sys
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from copy import deepcopy
from pathlib import Path

import requests

APP_DIR = Path(__file__).resolve().parent
TASKS_FILE = APP_DIR / "function-tasks.json"

# JS snippet to evaluate data.js and emit the seed state as JSON
_SEED_STATE_JS = """
const fs = require('fs');
const vm = require('vm');
const code = fs.readFileSync(process.argv[1], 'utf8');
vm.runInThisContext(code);
const seed = getSeedData();
process.stdout.write(JSON.stringify(seed));
"""


# ── helpers ──────────────────────────────────────────────────────────

def find_pres_by_title(state, title):
    for p in state["presentations"]:
        if p["title"] == title:
            return p
    raise ValueError(f"Presentation not found: {title!r}")


def find_slide(state, pres_id, order):
    for s in state["slides"]:
        if s["presentationId"] == pres_id and s["order"] == order:
            return s
    raise ValueError(f"Slide not found: presId={pres_id!r}, order={order}")


def get_slides_for_pres(state, pres_id):
    return sorted(
        [s for s in state["slides"] if s["presentationId"] == pres_id],
        key=lambda s: s["order"],
    )


def find_comment_by_content(state, pres_id, substring):
    for c in state["comments"]:
        if c["presentationId"] == pres_id and substring in c.get("content", ""):
            return c
    raise ValueError(f"Comment containing {substring!r} not found on {pres_id}")


def find_user_by_name(state, name):
    for u in state["users"]:
        if u["name"] == name:
            return u
    raise ValueError(f"User not found: {name!r}")


def next_pres_id(state):
    pid = state.get("_nextPresentationId", 19)
    state["_nextPresentationId"] = pid + 1
    return f"pres_{pid:03d}"


def next_slide_id(state):
    sid = state.get("_nextSlideId", 500)
    state["_nextSlideId"] = sid + 1
    return f"slide_{sid:05d}"


def next_element_id(state):
    eid = state.get("_nextElementId", 618)
    state["_nextElementId"] = eid + 1
    return f"elem_{eid:05d}"


def next_comment_id(state):
    cid = state.get("_nextCommentId", 41)
    state["_nextCommentId"] = cid + 1
    return f"cmt_{cid:03d}"


def next_reply_id(state):
    rid = state.get("_nextReplyId", 25)
    state["_nextReplyId"] = rid + 1
    return f"reply_{rid:03d}"


def next_template_id(state):
    tid = state.get("_nextTemplateId", 13)
    state["_nextTemplateId"] = tid + 1
    return f"tmpl_{tid:03d}"


NOW = "2026-03-18T12:00:00Z"


# ── solve functions ──────────────────────────────────────────────────

def solve_task_1(state):
    """Create presentation 'AI Strategy 2026' with description."""
    pid = next_pres_id(state)
    sid = next_slide_id(state)
    eid = next_element_id(state)
    state["presentations"].append({
        "id": pid, "title": "AI Strategy 2026",
        "description": "Company-wide AI adoption plan",
        "createdAt": NOW, "updatedAt": NOW,
        "createdBy": state["currentUserId"],
        "theme": "minimal", "tags": [], "starred": False,
        "status": "draft", "slideCount": 1,
        "shareSettings": {
            "visibility": "private", "allowComments": True,
            "allowEditing": False, "shareLink": "", "embedLink": "",
            "sharedWith": [state["currentUserId"]]
        }
    })
    state["slides"].append({
        "id": sid, "presentationId": pid, "order": 0,
        "layout": "title", "backgroundColor": "#ffffff",
        "transition": {"type": "none", "duration": 500},
        "speakerNotes": "",
        "elements": [{
            "id": eid, "type": "text", "x": 80, "y": 180, "width": 800, "height": 70,
            "rotation": 0, "opacity": 1, "locked": False,
            "content": "AI Strategy 2026", "shapeType": None,
            "fill": None, "stroke": None, "strokeWidth": 0, "cornerRadius": 0,
            "imageUrl": None, "imagePlaceholder": None,
            "style": {
                "fontFamily": "Inter", "fontSize": 48, "fontWeight": "bold",
                "color": "#1a1a2e", "textAlign": "center",
                "italic": False, "underline": False,
                "lineHeight": 1.2, "letterSpacing": -1, "listType": "none"
            },
            "animation": {"type": "none", "duration": 300, "delay": 0, "order": 0}
        }]
    })


def solve_task_2(state):
    """Create presentation 'Budget Review Q2' with tags and theme."""
    pid = next_pres_id(state)
    sid = next_slide_id(state)
    eid = next_element_id(state)
    state["presentations"].append({
        "id": pid, "title": "Budget Review Q2",
        "description": "",
        "createdAt": NOW, "updatedAt": NOW,
        "createdBy": state["currentUserId"],
        "theme": "corporate", "tags": ["finance", "quarterly"],
        "starred": False, "status": "draft", "slideCount": 1,
        "shareSettings": {
            "visibility": "private", "allowComments": True,
            "allowEditing": False, "shareLink": "", "embedLink": "",
            "sharedWith": [state["currentUserId"]]
        }
    })
    state["slides"].append({
        "id": sid, "presentationId": pid, "order": 0,
        "layout": "title", "backgroundColor": "#ffffff",
        "transition": {"type": "none", "duration": 500},
        "speakerNotes": "",
        "elements": [{
            "id": eid, "type": "text", "x": 80, "y": 180, "width": 800, "height": 70,
            "rotation": 0, "opacity": 1, "locked": False,
            "content": "Budget Review Q2", "shapeType": None,
            "fill": None, "stroke": None, "strokeWidth": 0, "cornerRadius": 0,
            "imageUrl": None, "imagePlaceholder": None,
            "style": {
                "fontFamily": "Inter", "fontSize": 48, "fontWeight": "bold",
                "color": "#1a1a2e", "textAlign": "center",
                "italic": False, "underline": False,
                "lineHeight": 1.2, "letterSpacing": -1, "listType": "none"
            },
            "animation": {"type": "none", "duration": 300, "delay": 0, "order": 0}
        }]
    })


def solve_task_3(state):
    """Delete 'Competitor Analysis Dashboard'."""
    pres = find_pres_by_title(state, "Competitor Analysis Dashboard")
    pid = pres["id"]
    state["presentations"] = [p for p in state["presentations"] if p["id"] != pid]
    state["slides"] = [s for s in state["slides"] if s["presentationId"] != pid]
    state["comments"] = [c for c in state["comments"] if c["presentationId"] != pid]


def solve_task_4(state):
    """Duplicate 'Design Sprint Week 12 Recap'."""
    src = find_pres_by_title(state, "Design Sprint Week 12 Recap")
    new_pid = next_pres_id(state)
    copy = deepcopy(src)
    copy["id"] = new_pid
    copy["title"] = src["title"] + " (Copy)"
    copy["createdAt"] = NOW
    copy["updatedAt"] = NOW
    copy["status"] = "draft"
    copy["starred"] = False
    state["presentations"].append(copy)
    src_slides = get_slides_for_pres(state, src["id"])
    for slide in src_slides:
        new_slide = deepcopy(slide)
        new_slide["id"] = next_slide_id(state)
        new_slide["presentationId"] = new_pid
        new_slide["elements"] = [
            dict(el, id=next_element_id(state)) for el in new_slide["elements"]
        ]
        state["slides"].append(new_slide)


def solve_task_5(state):
    find_pres_by_title(state, "Engineering Architecture Overview")["starred"] = True


def solve_task_6(state):
    find_pres_by_title(state, "Q1 2026 Product Roadmap")["starred"] = False


def solve_task_7(state):
    find_pres_by_title(state, "Design Workshop Materials")["status"] = "published"


def solve_task_8(state):
    find_pres_by_title(state, "Q4 2025 Revenue Analysis")["status"] = "archived"


def solve_task_9(state):
    find_pres_by_title(state, "Brand Identity Guidelines v2.0")["shareSettings"]["visibility"] = "public"


def solve_task_10(state):
    find_pres_by_title(state, "Annual Company All-Hands 2026")["shareSettings"]["allowComments"] = False


def solve_task_11(state):
    find_pres_by_title(state, "Q1 2026 Product Roadmap")["shareSettings"]["allowEditing"] = True


def solve_task_12(state):
    pres = find_pres_by_title(state, "Series B Fundraising Pitch")
    if "user_002" not in pres["shareSettings"]["sharedWith"]:
        pres["shareSettings"]["sharedWith"].append("user_002")


def solve_task_13(state):
    pres = find_pres_by_title(state, "Client Proposal \u2014 TechVentures Redesign")
    pres["shareSettings"]["sharedWith"] = [
        u for u in pres["shareSettings"]["sharedWith"] if u != "user_003"
    ]


def solve_task_14(state):
    pres = find_pres_by_title(state, "Onboarding Training Module")
    pres["shareSettings"]["visibility"] = "team"
    pres["shareSettings"]["allowComments"] = True


def solve_task_15(state):
    pres = find_pres_by_title(state, "Design Sprint Week 12 Recap")
    slides = get_slides_for_pres(state, pres["id"])
    state["slides"].append({
        "id": next_slide_id(state), "presentationId": pres["id"],
        "order": len(slides), "layout": "blank", "backgroundColor": "#ffffff",
        "transition": {"type": "none", "duration": 500},
        "speakerNotes": "", "elements": []
    })
    pres["slideCount"] = len(slides) + 1


def solve_task_16(state):
    pres = find_pres_by_title(state, "Team Retrospective \u2014 Sprint 47")
    slides = get_slides_for_pres(state, pres["id"])
    last = slides[-1]
    state["slides"] = [s for s in state["slides"] if s["id"] != last["id"]]
    state["comments"] = [c for c in state["comments"] if c["slideId"] != last["id"]]
    pres["slideCount"] = len(slides) - 1


def solve_task_17(state):
    pres = find_pres_by_title(state, "Q1 2026 Product Roadmap")
    slides = get_slides_for_pres(state, pres["id"])
    first = slides[0]
    for s in slides:
        if s["order"] > first["order"]:
            s["order"] += 1
    new_slide = deepcopy(first)
    new_slide["id"] = next_slide_id(state)
    new_slide["order"] = first["order"] + 1
    new_slide["elements"] = [dict(el, id=next_element_id(state)) for el in new_slide["elements"]]
    state["slides"].append(new_slide)
    pres["slideCount"] = len(slides) + 1


def solve_task_18(state):
    pres = find_pres_by_title(state, "Q1 2026 Product Roadmap")
    find_slide(state, pres["id"], 1)["layout"] = "two-column"


def solve_task_19(state):
    pres = find_pres_by_title(state, "Q1 2026 Product Roadmap")
    find_slide(state, pres["id"], 0)["backgroundColor"] = "#7B61FF"


def solve_task_20(state):
    pres = find_pres_by_title(state, "Q1 2026 Product Roadmap")
    find_slide(state, pres["id"], 2)["speakerNotes"] = "Highlight the three major product launches and their specific impact metrics."


def solve_task_21(state):
    pres = find_pres_by_title(state, "Q1 2026 Product Roadmap")
    find_slide(state, pres["id"], 1)["transition"]["type"] = "dissolve"


def solve_task_22(state):
    pres = find_pres_by_title(state, "Q1 2026 Product Roadmap")
    find_slide(state, pres["id"], 5)["transition"] = {"type": "push", "duration": 800}


def solve_task_23(state):
    pres = find_pres_by_title(state, "Q1 2026 Product Roadmap")
    find_slide(state, pres["id"], 2)["elements"][0]["content"] = "Q1 Major Launches"


def solve_task_24(state):
    pres = find_pres_by_title(state, "Q1 2026 Product Roadmap")
    find_slide(state, pres["id"], 0)["elements"][0]["style"]["fontFamily"] = "Poppins"


def solve_task_25(state):
    pres = find_pres_by_title(state, "Q1 2026 Product Roadmap")
    find_slide(state, pres["id"], 2)["elements"][0]["style"]["fontSize"] = 40


def solve_task_26(state):
    pres = find_pres_by_title(state, "Q1 2026 Product Roadmap")
    find_slide(state, pres["id"], 0)["elements"][1]["style"]["fontWeight"] = "600"


def solve_task_27(state):
    pres = find_pres_by_title(state, "Q1 2026 Product Roadmap")
    find_slide(state, pres["id"], 8)["elements"][0]["style"]["color"] = "#F24822"


def solve_task_28(state):
    pres = find_pres_by_title(state, "Q1 2026 Product Roadmap")
    find_slide(state, pres["id"], 0)["elements"][1]["style"]["italic"] = True


def solve_task_29(state):
    pres = find_pres_by_title(state, "Q1 2026 Product Roadmap")
    find_slide(state, pres["id"], 2)["elements"][0]["style"]["underline"] = True


def solve_task_30(state):
    pres = find_pres_by_title(state, "Q1 2026 Product Roadmap")
    find_slide(state, pres["id"], 0)["elements"][1]["style"]["textAlign"] = "left"


def solve_task_31(state):
    pres = find_pres_by_title(state, "Q1 2026 Product Roadmap")
    find_slide(state, pres["id"], 2)["elements"][1]["style"]["listType"] = "numbered"


def solve_task_32(state):
    pres = find_pres_by_title(state, "Q1 2026 Product Roadmap")
    find_slide(state, pres["id"], 1)["elements"][0]["locked"] = True


def solve_task_33(state):
    pres = find_pres_by_title(state, "Q1 2026 Product Roadmap")
    find_slide(state, pres["id"], 2)["elements"][0]["style"]["letterSpacing"] = 2


def solve_task_34(state):
    pres = find_pres_by_title(state, "Q1 2026 Product Roadmap")
    find_slide(state, pres["id"], 0)["elements"][0]["style"]["lineHeight"] = 2.0


def solve_task_35(state):
    pres = find_pres_by_title(state, "Q1 2026 Product Roadmap")
    slide = find_slide(state, pres["id"], 3)
    for el in slide["elements"]:
        if el["type"] == "shape" and el.get("shapeType") == "rectangle":
            el["fill"] = "#0D99FF"
            break


def solve_task_36(state):
    pres = find_pres_by_title(state, "Q1 2026 Product Roadmap")
    slide = find_slide(state, pres["id"], 1)
    for el in slide["elements"]:
        if el["type"] == "shape" and el.get("shapeType") == "line":
            el["stroke"] = "#14AE5C"
            break


def solve_task_37(state):
    pres = find_pres_by_title(state, "Q1 2026 Product Roadmap")
    slide = find_slide(state, pres["id"], 4)
    for el in slide["elements"]:
        if el["type"] == "shape" and el.get("shapeType") == "rectangle":
            el["shapeType"] = "circle"
            break


def solve_task_38(state):
    pres = find_pres_by_title(state, "Q1 2026 Product Roadmap")
    find_slide(state, pres["id"], 0)["elements"][0]["opacity"] = 0.5


def solve_task_39(state):
    pres = find_pres_by_title(state, "Q1 2026 Product Roadmap")
    find_slide(state, pres["id"], 0)["elements"][0]["rotation"] = 45


def solve_task_40(state):
    pres = find_pres_by_title(state, "Q1 2026 Product Roadmap")
    slide = find_slide(state, pres["id"], 0)
    slide["elements"] = [
        el for el in slide["elements"]
        if not (el["type"] == "shape" and el.get("shapeType") == "line")
    ]


def solve_task_41(state):
    pres = find_pres_by_title(state, "Q1 2026 Product Roadmap")
    slide = find_slide(state, pres["id"], 0)
    eid = next_element_id(state)
    slide["elements"].append({
        "id": eid, "type": "text", "x": 100, "y": 100, "width": 300, "height": 60,
        "rotation": 0, "opacity": 1, "locked": False,
        "content": "Double-click to edit", "shapeType": None,
        "fill": None, "stroke": None, "strokeWidth": 0, "cornerRadius": 0,
        "imageUrl": None, "imagePlaceholder": None,
        "style": {
            "fontFamily": "Inter", "fontSize": 20, "fontWeight": "normal",
            "color": "#2c2c2c", "textAlign": "left",
            "italic": False, "underline": False,
            "lineHeight": 1.4, "letterSpacing": 0, "listType": "none"
        },
        "animation": {"type": "none", "duration": 300, "delay": 0, "order": 0}
    })


def solve_task_42(state):
    pres = find_pres_by_title(state, "Q1 2026 Product Roadmap")
    slide = find_slide(state, pres["id"], 0)
    eid = next_element_id(state)
    slide["elements"].append({
        "id": eid, "type": "shape", "x": 100, "y": 100, "width": 200, "height": 150,
        "rotation": 0, "opacity": 1, "locked": False,
        "content": None, "shapeType": "rectangle", "fill": "#4A90D9",
        "stroke": "#333333", "strokeWidth": 2, "cornerRadius": 0,
        "imageUrl": None, "imagePlaceholder": None, "style": None,
        "animation": {"type": "none", "duration": 300, "delay": 0, "order": 0}
    })


def solve_task_43(state):
    pres = find_pres_by_title(state, "Q1 2026 Product Roadmap")
    slide = find_slide(state, pres["id"], 0)
    eid = next_element_id(state)
    slide["elements"].append({
        "id": eid, "type": "image", "x": 100, "y": 100, "width": 300, "height": 200,
        "rotation": 0, "opacity": 1, "locked": False,
        "content": None, "shapeType": None, "fill": None,
        "stroke": None, "strokeWidth": 0, "cornerRadius": 0,
        "imageUrl": None, "imagePlaceholder": "#e0e0e0", "style": None,
        "animation": {"type": "none", "duration": 300, "delay": 0, "order": 0}
    })


def solve_task_44(state):
    pres = find_pres_by_title(state, "Q1 2026 Product Roadmap")
    find_slide(state, pres["id"], 2)["elements"][0]["animation"]["type"] = "fade-in"


def solve_task_45(state):
    pres = find_pres_by_title(state, "Q1 2026 Product Roadmap")
    find_slide(state, pres["id"], 8)["elements"][0]["animation"] = {
        "type": "bounce-in", "duration": 500, "delay": 200, "order": 0
    }


def solve_task_46(state):
    pres = find_pres_by_title(state, "Q1 2026 Product Roadmap")
    slides = get_slides_for_pres(state, pres["id"])
    cid = next_comment_id(state)
    state["comments"].append({
        "id": cid, "presentationId": pres["id"],
        "slideId": slides[0]["id"], "elementId": None,
        "authorId": state["currentUserId"],
        "content": "Great progress on the roadmap!",
        "createdAt": NOW, "resolved": False, "replies": []
    })


def solve_task_47(state):
    pres = find_pres_by_title(state, "Q1 2026 Product Roadmap")
    comment = find_comment_by_content(state, pres["id"], "chart visualization")
    rid = next_reply_id(state)
    comment["replies"].append({
        "id": rid, "authorId": state["currentUserId"],
        "content": "I agree, a bar chart would work best for this data.",
        "createdAt": NOW
    })


def solve_task_48(state):
    pres = find_pres_by_title(state, "Q1 2026 Product Roadmap")
    find_comment_by_content(state, pres["id"], "Canva")["resolved"] = True


def solve_task_49(state):
    pres = find_pres_by_title(state, "Series B Fundraising Pitch")
    find_comment_by_content(state, pres["id"], "Finance team confirmed")["resolved"] = False


def solve_task_50(state):
    pres = find_pres_by_title(state, "Q1 2026 Product Roadmap")
    state["comments"] = [
        c for c in state["comments"]
        if not (c["presentationId"] == pres["id"] and "Love the design" in c.get("content", ""))
    ]


def solve_task_51(state):
    pres = find_pres_by_title(state, "Brand Identity Guidelines v2.0")
    find_comment_by_content(state, pres["id"], "logo clear space")["resolved"] = True


def solve_task_52(state):
    pres = find_pres_by_title(state, "Q1 2026 Product Roadmap")
    slide = find_slide(state, pres["id"], 8)
    tid = next_template_id(state)
    elements_copy = deepcopy(slide["elements"])
    for el in elements_copy:
        if "id" in el:
            del el["id"]
    state["templates"].append({
        "id": tid, "name": "Three Cards Layout", "category": "custom",
        "layout": slide["layout"],
        "description": "Custom template saved from slide",
        "previewColor": slide["backgroundColor"] if slide["backgroundColor"] != "#ffffff" else "#7B61FF",
        "elements": elements_copy
    })


def solve_task_53(state):
    pres = find_pres_by_title(state, "Q1 2026 Product Roadmap")
    slide = find_slide(state, pres["id"], 3)
    tid = next_template_id(state)
    elements_copy = deepcopy(slide["elements"])
    for el in elements_copy:
        if "id" in el:
            del el["id"]
    state["templates"].append({
        "id": tid, "name": "Metrics Dashboard", "category": "custom",
        "layout": slide["layout"],
        "description": "Custom template saved from slide",
        "previewColor": slide["backgroundColor"] if slide["backgroundColor"] != "#ffffff" else "#7B61FF",
        "elements": elements_copy
    })


def solve_task_54(state):
    pres_002 = find_pres_by_title(state, "Brand Identity Guidelines v2.0")
    creator_id = pres_002["createdBy"]
    pres_005 = find_pres_by_title(state, "Engineering Architecture Overview")
    if creator_id not in pres_005["shareSettings"]["sharedWith"]:
        pres_005["shareSettings"]["sharedWith"].append(creator_id)


def solve_task_55(state):
    for pres in state["presentations"]:
        if pres["status"] == "draft":
            pres["starred"] = True


SOLVERS = {f"task_{i}": globals()[f"solve_task_{i}"] for i in range(1, 56)}


# ── server management ────────────────────────────────────────────────

def generate_seed_state():
    data_js = str(APP_DIR / "js" / "data.js")
    result = subprocess.run(
        ["node", "-e", _SEED_STATE_JS, data_js],
        capture_output=True, text=True,
    )
    if result.returncode != 0:
        raise RuntimeError(f"Failed to generate seed state:\n{result.stderr}")
    return json.loads(result.stdout)


def seed_server(server_url, seed_state):
    resp = requests.put(
        f"{server_url}/api/state", json=seed_state,
        headers={"Content-Type": "application/json"},
    )
    if resp.status_code != 200:
        raise RuntimeError(f"Failed to seed server: HTTP {resp.status_code}")


def find_free_port(start=9000):
    port = start
    while port < start + 200:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            try:
                s.bind(("", port))
                return port
            except OSError:
                port += 1
    raise RuntimeError(f"No free port found in range {start}-{start+200}")


def start_server(port):
    proc = subprocess.Popen(
        [sys.executable, "server.py", "--port", str(port)],
        cwd=str(APP_DIR),
        stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
    )
    for _ in range(30):
        try:
            requests.get(f"http://localhost:{port}/", timeout=1)
            return proc
        except (requests.ConnectionError, requests.Timeout):
            time.sleep(0.2)
    proc.kill()
    raise RuntimeError(f"Server failed to start on port {port}")


def stop_server(proc):
    if proc and proc.poll() is None:
        proc.terminate()
        try:
            proc.wait(timeout=5)
        except subprocess.TimeoutExpired:
            proc.kill()


# ── task runner ──────────────────────────────────────────────────────

def load_tasks():
    with open(TASKS_FILE) as f:
        return json.load(f)


def load_verifier(verify_path):
    full_path = APP_DIR / verify_path
    spec = importlib.util.spec_from_file_location("verifier", str(full_path))
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.verify


def run_single_task(task, server_url):
    task_id = task["id"]
    solver = SOLVERS.get(task_id)
    if not solver:
        return task_id, False, f"No solver defined for {task_id}"
    try:
        resp = requests.post(f"{server_url}/api/reset")
        if resp.status_code != 200:
            return task_id, False, f"Reset failed: HTTP {resp.status_code}"
        time.sleep(0.3)
        resp = requests.get(f"{server_url}/api/state")
        if resp.status_code != 200:
            return task_id, False, f"Could not read state after reset: HTTP {resp.status_code}"
        state = resp.json()
        solver(state)
        resp = requests.put(
            f"{server_url}/api/state", json=state,
            headers={"Content-Type": "application/json"},
        )
        if resp.status_code != 200:
            return task_id, False, f"Could not write state: HTTP {resp.status_code}"
        verify_fn = load_verifier(task["verify"])
        passed, message = verify_fn(server_url)
        return task_id, passed, message
    except Exception as e:
        return task_id, False, f"Exception: {e}"


def run_tasks_sequential(tasks, port, seed_state):
    proc = start_server(port)
    server_url = f"http://localhost:{port}"
    results = []
    try:
        seed_server(server_url, seed_state)
        for task in tasks:
            result = run_single_task(task, server_url)
            results.append(result)
            status = "\033[32m  PASS\033[0m" if result[1] else "\033[31m  FAIL\033[0m"
            print(f"{status}  {result[0]:12s}  {result[2]}")
    finally:
        stop_server(proc)
    return results


def run_tasks_parallel(tasks, workers, base_port, seed_state):
    results = []

    def worker_fn(task, port):
        proc = start_server(port)
        server_url = f"http://localhost:{port}"
        try:
            seed_server(server_url, seed_state)
            return run_single_task(task, server_url)
        finally:
            stop_server(proc)

    with ThreadPoolExecutor(max_workers=workers) as executor:
        futures = {}
        for i, task in enumerate(tasks):
            port = base_port + i
            future = executor.submit(worker_fn, task, port)
            futures[future] = task["id"]
        for future in as_completed(futures):
            result = future.result()
            results.append(result)
            status = "\033[32m  PASS\033[0m" if result[1] else "\033[31m  FAIL\033[0m"
            print(f"{status}  {result[0]:12s}  {result[2]}")
    return results


# ── main ─────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="Figma Slides function-task sanity check")
    parser.add_argument("--task-id", type=str, help="Run a single task by ID")
    parser.add_argument("--workers", type=int, default=1, help="Number of parallel workers")
    parser.add_argument("--port", type=int, default=9500, help="Base port for servers")
    args = parser.parse_args()

    tasks = load_tasks()
    if args.task_id:
        tasks = [t for t in tasks if t["id"] == args.task_id]
        if not tasks:
            print(f"Task '{args.task_id}' not found.")
            sys.exit(1)

    print("Generating seed state from JS data...")
    seed_state = generate_seed_state()
    print(f"Running {len(tasks)} task(s)...\n")

    if args.workers <= 1:
        port = find_free_port(args.port)
        results = run_tasks_sequential(tasks, port, seed_state)
    else:
        results = run_tasks_parallel(tasks, args.workers, args.port, seed_state)

    passed = sum(1 for _, p, _ in results if p)
    total = len(results)
    failed = [tid for tid, p, _ in results if not p]

    print(f"\n{passed}/{total} passed")
    if failed:
        print(f"Failed: {', '.join(failed)}")
        sys.exit(1)
    else:
        sys.exit(0)


if __name__ == "__main__":
    main()
