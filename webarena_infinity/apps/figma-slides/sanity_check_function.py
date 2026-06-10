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
import signal
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

const state = {
    slides: JSON.parse(JSON.stringify(SLIDES)),
    deckSettings: JSON.parse(JSON.stringify(DECK_SETTINGS)),
    templateStyles: JSON.parse(JSON.stringify(TEMPLATE_STYLES)),
    comments: JSON.parse(JSON.stringify(COMMENTS)),
    libraries: JSON.parse(JSON.stringify(LIBRARIES)),
    collaborators: JSON.parse(JSON.stringify(COLLABORATORS)),
    currentUser: JSON.parse(JSON.stringify(CURRENT_USER)),
    exportHistory: JSON.parse(JSON.stringify(EXPORT_HISTORY)),
    versionHistory: JSON.parse(JSON.stringify(VERSION_HISTORY)),
    availableTemplates: JSON.parse(JSON.stringify(AVAILABLE_TEMPLATES)),
    _seedVersion: SEED_DATA_VERSION,
    _nextSlideOrder: 16,
    _nextCommentId: 7,
    _nextObjectId: 200
};
process.stdout.write(JSON.stringify(state));
"""


# ── helpers ──────────────────────────────────────────────────────────

def find_entity(entities, **kwargs):
    """Find an entity by attribute match. Raises if not found."""
    for e in entities:
        if all(e.get(k) == v for k, v in kwargs.items()):
            return e
    raise ValueError(f"Entity not found: {kwargs}")


def find_slide(state, slide_id):
    """Find a slide by ID."""
    for s in state["slides"]:
        if s["id"] == slide_id:
            return s
    raise ValueError(f"Slide not found: {slide_id}")


def find_slide_by_title(state, title):
    """Find a slide by title."""
    for s in state["slides"]:
        if s["title"] == title:
            return s
    raise ValueError(f"Slide not found by title: {title}")


def find_object(slide, obj_id):
    """Find an object in a slide by ID."""
    for o in slide["objects"]:
        if o["id"] == obj_id:
            return o
    raise ValueError(f"Object not found: {obj_id} in slide {slide['id']}")


def find_comment(state, comment_id):
    """Find a comment by ID."""
    for c in state["comments"]:
        if c["id"] == comment_id:
            return c
    raise ValueError(f"Comment not found: {comment_id}")


def find_collaborator(state, user_id):
    """Find a collaborator by user ID."""
    for c in state["collaborators"]:
        if c["id"] == user_id:
            return c
    raise ValueError(f"Collaborator not found: {user_id}")


def find_template_style(state, style_id):
    """Find a template style by ID."""
    for s in state["templateStyles"]:
        if s["id"] == style_id:
            return s
    raise ValueError(f"Template style not found: {style_id}")


def find_library(state, lib_id):
    """Find a library by ID."""
    for lib in state["libraries"]:
        if lib["id"] == lib_id:
            return lib
    raise ValueError(f"Library not found: {lib_id}")


# ── solve functions ──────────────────────────────────────────────────

def solve_task_1(state):
    """Rename slide 'Agenda' to 'Meeting Agenda'."""
    slide = find_slide(state, "slide_002")
    slide["title"] = "Meeting Agenda"


def solve_task_2(state):
    """Update presenter notes on slide 'Q4 Roadmap'."""
    slide = find_slide(state, "slide_006")
    slide["presenterNotes"] = "Aiko will present the roadmap. Focus on timelines and deliverables."


def solve_task_3(state):
    """Skip slide 'Competitive Landscape'."""
    slide = find_slide(state, "slide_013")
    slide["skipped"] = True


def solve_task_4(state):
    """Unskip slide 'Sprint Timeline'."""
    slide = find_slide(state, "slide_012")
    slide["skipped"] = False


def solve_task_5(state):
    """Delete slide 'Sprint Timeline'."""
    deleted_order = None
    deleted_id = "slide_012"
    for s in state["slides"]:
        if s["id"] == deleted_id:
            deleted_order = s["order"]
            break
    state["slides"] = [s for s in state["slides"] if s["id"] != deleted_id]
    if deleted_order is not None:
        for s in state["slides"]:
            if s["order"] > deleted_order:
                s["order"] -= 1
    # Remove comments for deleted slide
    state["comments"] = [c for c in state["comments"] if c["slideId"] != deleted_id]


def solve_task_6(state):
    """Duplicate slide 'Q3 Highlights'."""
    source = find_slide(state, "slide_003")
    dup = deepcopy(source)
    dup["id"] = "slide_dup_003"
    dup["order"] = source["order"] + 1
    dup["title"] = source["title"] + " (copy)"
    next_obj_id = state.get("_nextObjectId", 200)
    for obj in dup["objects"]:
        obj["id"] = f"obj_{next_obj_id}"
        next_obj_id += 1
    state["_nextObjectId"] = next_obj_id
    # Shift orders for slides after the source
    for s in state["slides"]:
        if s["order"] > source["order"]:
            s["order"] += 1
    state["slides"].append(dup)
    state["_nextSlideOrder"] = state.get("_nextSlideOrder", 16) + 1


def solve_task_7(state):
    """Rename group 'Q3 Review' to 'Q3 Performance Review'."""
    for s in state["slides"]:
        if s.get("groupId") == "group_001":
            s["groupName"] = "Q3 Performance Review"


def solve_task_8(state):
    """Add new blank slide after 'Agenda'."""
    agenda = find_slide(state, "slide_002")
    after_order = agenda["order"]
    for s in state["slides"]:
        if s["order"] > after_order:
            s["order"] += 1
    new_slide = {
        "id": "slide_new_after_agenda",
        "order": after_order + 1,
        "title": "Untitled Slide",
        "layout": "layout_blank",
        "templateStyle": state["deckSettings"]["defaultTemplateStyle"],
        "skipped": False,
        "groupId": agenda.get("groupId"),
        "groupName": agenda.get("groupName"),
        "background": {"type": "solid", "color": "#1E1E1E"},
        "presenterNotes": "",
        "transition": deepcopy(state["deckSettings"]["defaultTransition"]),
        "slideNumberEnabled": state["deckSettings"]["slideNumbersEnabled"],
        "slideNumberCount": state["deckSettings"]["slideNumberCount"],
        "slideNumberFormat": state["deckSettings"]["slideNumberFormat"],
        "slideNumberIncludeTotal": state["deckSettings"]["slideNumberIncludeTotal"],
        "objects": []
    }
    state["slides"].append(new_slide)
    state["_nextSlideOrder"] = state.get("_nextSlideOrder", 16) + 1


def solve_task_9(state):
    """Change background of 'Agenda' to solid #2D2D2D."""
    slide = find_slide(state, "slide_002")
    slide["background"] = {"type": "solid", "color": "#2D2D2D"}


def solve_task_10(state):
    """Set background of 'Next Steps' to gradient."""
    slide = find_slide(state, "slide_015")
    slide["background"] = {
        "type": "gradient",
        "gradient": {
            "type": "linear",
            "angle": 90,
            "stops": [
                {"color": "#1E1E1E", "position": 0},
                {"color": "#0052CC", "position": 100}
            ]
        }
    }


def solve_task_11(state):
    """Change 'Customer Feedback' background to solid."""
    slide = find_slide(state, "slide_005")
    slide["background"] = {"type": "solid", "color": "#2D1B69"}


def solve_task_12(state):
    """Change transition of 'Agenda' to push/left."""
    slide = find_slide(state, "slide_002")
    slide["transition"]["type"] = "push"
    slide["transition"]["direction"] = "left"


def solve_task_13(state):
    """Set transition duration of 'Q3 Highlights' to 800ms."""
    slide = find_slide(state, "slide_003")
    slide["transition"]["duration"] = 800


def solve_task_14(state):
    """Set transition easing of 'Design System 2.0' to spring."""
    slide = find_slide(state, "slide_007")
    slide["transition"]["easing"] = "spring"


def solve_task_15(state):
    """Set default deck transition to push/left."""
    state["deckSettings"]["defaultTransition"]["type"] = "push"
    state["deckSettings"]["defaultTransition"]["direction"] = "left"


def solve_task_16(state):
    """Change title text on slide 1."""
    slide = find_slide(state, "slide_001")
    obj = find_object(slide, "obj_001")
    obj["text"] = "Q4 2025 Strategic Plan"


def solve_task_17(state):
    """Change font size of title on Agenda."""
    slide = find_slide(state, "slide_002")
    obj = find_object(slide, "obj_010")
    obj["fontSize"] = 42


def solve_task_18(state):
    """Change font family of subtitle on slide 1."""
    slide = find_slide(state, "slide_001")
    obj = find_object(slide, "obj_002")
    obj["fontFamily"] = "DM Sans"


def solve_task_19(state):
    """Set opacity of Date text on slide 1 to 50."""
    slide = find_slide(state, "slide_001")
    obj = find_object(slide, "obj_003")
    obj["opacity"] = 50


def solve_task_20(state):
    """Lock title on slide 1."""
    slide = find_slide(state, "slide_001")
    obj = find_object(slide, "obj_001")
    obj["locked"] = True


def solve_task_21(state):
    """Change text alignment of Quote on Customer Feedback to left."""
    slide = find_slide(state, "slide_005")
    obj = find_object(slide, "obj_040")
    obj["textAlign"] = "left"


def solve_task_22(state):
    """Change fill color of Metric Card 1 on Q3 Highlights."""
    slide = find_slide(state, "slide_003")
    obj = find_object(slide, "obj_021")
    obj["fill"] = "#7B61FF"


def solve_task_23(state):
    """Change text color of Section Title on Q4 Roadmap."""
    slide = find_slide(state, "slide_006")
    obj = find_object(slide, "obj_050")
    obj["color"] = "#FFD700"


def solve_task_24(state):
    """Rotate Accent Line on Agenda by 45 degrees."""
    slide = find_slide(state, "slide_002")
    obj = find_object(slide, "obj_012")
    obj["rotation"] = 45


def solve_task_25(state):
    """Change font weight of title on Next Steps to 600."""
    slide = find_slide(state, "slide_015")
    obj = find_object(slide, "obj_140")
    obj["fontWeight"] = 600


def solve_task_26(state):
    """Delete Date text from slide 1."""
    slide = find_slide(state, "slide_001")
    slide["objects"] = [o for o in slide["objects"] if o["id"] != "obj_003"]


def solve_task_27(state):
    """Delete Risk 3 from Key Risks & Mitigations."""
    slide = find_slide(state, "slide_014")
    slide["objects"] = [o for o in slide["objects"] if o["id"] != "obj_133"]


def solve_task_28(state):
    """Update cell in adoption table to 95%."""
    slide = find_slide(state, "slide_010")
    obj = find_object(slide, "obj_091")
    obj["cells"][1][4] = "95%"


def solve_task_29(state):
    """Add row to adoption table."""
    slide = find_slide(state, "slide_010")
    obj = find_object(slide, "obj_091")
    obj["cells"].append([""] * obj["columns"])
    obj["rows"] += 1


def solve_task_30(state):
    """Add column to comparison table."""
    slide = find_slide(state, "slide_013")
    obj = find_object(slide, "obj_121")
    for row in obj["cells"]:
        row.append("")
    obj["columns"] += 1


def solve_task_31(state):
    """Delete last row (API Access) from comparison table."""
    slide = find_slide(state, "slide_013")
    obj = find_object(slide, "obj_121")
    obj["cells"].pop()
    obj["rows"] -= 1


def solve_task_32(state):
    """Update AI Features/DesignCraft cell to 'Advanced'."""
    slide = find_slide(state, "slide_013")
    obj = find_object(slide, "obj_121")
    obj["cells"][4][1] = "Advanced"


def solve_task_33(state):
    """Change code language to TypeScript."""
    slide = find_slide(state, "slide_008")
    obj = find_object(slide, "obj_071")
    obj["language"] = "TypeScript"


def solve_task_34(state):
    """Change code theme to dracula."""
    slide = find_slide(state, "slide_008")
    obj = find_object(slide, "obj_071")
    obj["theme"] = "dracula"


def solve_task_35(state):
    """Update code content."""
    slide = find_slide(state, "slide_008")
    obj = find_object(slide, "obj_071")
    obj["code"] = 'console.log("Hello World");'


def solve_task_36(state):
    """Add bounce animation to Agenda List."""
    slide = find_slide(state, "slide_002")
    obj = find_object(slide, "obj_011")
    obj["animation"] = {
        "style": "bounce",
        "duration": 500,
        "timing": "on_click",
        "direction": "in",
        "order": 0
    }


def solve_task_37(state):
    """Remove animation from title on slide 1."""
    slide = find_slide(state, "slide_001")
    obj = find_object(slide, "obj_001")
    obj["animation"] = None


def solve_task_38(state):
    """Change animation duration of Timeline Badge to 600ms."""
    slide = find_slide(state, "slide_007")
    obj = find_object(slide, "obj_062")
    obj["animation"]["duration"] = 600


def solve_task_39(state):
    """Add comment on slide Q4 Roadmap."""
    next_id = state.get("_nextCommentId", 7)
    comment = {
        "id": f"comment_{str(next_id).zfill(3)}",
        "slideId": "slide_006",
        "userId": state["currentUser"]["id"],
        "userName": state["currentUser"]["name"],
        "avatarColor": state["currentUser"]["avatarColor"],
        "text": "We should add budget numbers here.",
        "createdAt": "2026-03-07T12:00:00Z",
        "resolved": False,
        "replies": [],
        "position": {"x": 400, "y": 300}
    }
    state["comments"].append(comment)
    state["_nextCommentId"] = next_id + 1


def solve_task_40(state):
    """Resolve comment_001."""
    comment = find_comment(state, "comment_001")
    comment["resolved"] = True


def solve_task_41(state):
    """Reply to comment_002."""
    comment = find_comment(state, "comment_002")
    comment["replies"].append({
        "id": "reply_sanity",
        "userId": state["currentUser"]["id"],
        "userName": state["currentUser"]["name"],
        "avatarColor": state["currentUser"]["avatarColor"],
        "text": "Great idea, I will add one after the roadmap section.",
        "createdAt": "2026-03-07T12:00:00Z"
    })


def solve_task_42(state):
    """Delete comment_006."""
    state["comments"] = [c for c in state["comments"] if c["id"] != "comment_006"]


def solve_task_43(state):
    """Unresolve comment_003."""
    comment = find_comment(state, "comment_003")
    comment["resolved"] = False


def solve_task_44(state):
    """Change Tom Nguyen role to Editor."""
    collab = find_collaborator(state, "user_006")
    collab["role"] = "Editor"


def solve_task_45(state):
    """Remove James O'Brien."""
    state["collaborators"] = [c for c in state["collaborators"] if c["id"] != "user_004"]


def solve_task_46(state):
    """Change David Park role to Viewer."""
    collab = find_collaborator(state, "user_008")
    collab["role"] = "Viewer"


def solve_task_47(state):
    """Rename Minimal Dark to Midnight Dark."""
    style = find_template_style(state, "ts_001")
    style["name"] = "Midnight Dark"


def solve_task_48(state):
    """Change Primary color in Corporate Blue to #0066FF."""
    style = find_template_style(state, "ts_002")
    for color in style["colors"]:
        if color["id"] == "tc_013":
            color["value"] = "#0066FF"
            break


def solve_task_49(state):
    """Add Highlight color to Warm Sunset."""
    style = find_template_style(state, "ts_003")
    style["colors"].append({
        "id": "tc_new_highlight",
        "name": "Highlight",
        "value": "#FFD700"
    })


def solve_task_50(state):
    """Remove Caption text style from Minimal Dark."""
    style = find_template_style(state, "ts_001")
    style["textStyles"] = [t for t in style["textStyles"] if t["id"] != "txt_005"]


def solve_task_51(state):
    """Disable Presentation Icons Pack."""
    lib = find_library(state, "lib_003")
    lib["enabled"] = False


def solve_task_52(state):
    """Remove Brand Assets 2025."""
    state["libraries"] = [l for l in state["libraries"] if l["id"] != "lib_002"]


def solve_task_53(state):
    """Rename deck."""
    state["deckSettings"]["name"] = "Q4 2025 Product Strategy & Roadmap"


def solve_task_54(state):
    """Change aspect ratio to 4:3."""
    state["deckSettings"]["aspectRatio"] = "4:3"
    state["deckSettings"]["width"] = 1024
    state["deckSettings"]["height"] = 768


def solve_task_55(state):
    """Disable download in share settings."""
    state["deckSettings"]["shareSettings"]["allowDownload"] = False


def solve_task_56(state):
    """Toggle available offline."""
    state["deckSettings"]["availableOffline"] = True


def solve_task_57(state):
    """Change slide number format on Q3 Highlights to with_total."""
    slide = find_slide(state, "slide_003")
    slide["slideNumberFormat"] = "with_total"


def solve_task_58(state):
    """Enable slide numbers on Thank You slide."""
    slide = find_slide(state, "slide_016")
    slide["slideNumberEnabled"] = True


def solve_task_59(state):
    """Vote for Performance improvements in poll."""
    slide = find_slide(state, "slide_009")
    obj = find_object(slide, "obj_081")
    for option in obj["options"]:
        if option["id"] == "opt_02":
            option["votes"] += 1
            break


def solve_task_60(state):
    """Add alignment response value 4."""
    slide = find_slide(state, "slide_009")
    obj = find_object(slide, "obj_082")
    obj["responses"].append({"userId": "user_001", "value": 4})


def solve_task_61(state):
    """Add thumbsUp stamp."""
    slide = find_slide(state, "slide_016")
    obj = find_object(slide, "obj_152")
    obj["stamps"].append({"userId": "user_001", "type": "thumbsUp"})


SOLVERS = {
    "task_1": solve_task_1,
    "task_2": solve_task_2,
    "task_3": solve_task_3,
    "task_4": solve_task_4,
    "task_5": solve_task_5,
    "task_6": solve_task_6,
    "task_7": solve_task_7,
    "task_8": solve_task_8,
    "task_9": solve_task_9,
    "task_10": solve_task_10,
    "task_11": solve_task_11,
    "task_12": solve_task_12,
    "task_13": solve_task_13,
    "task_14": solve_task_14,
    "task_15": solve_task_15,
    "task_16": solve_task_16,
    "task_17": solve_task_17,
    "task_18": solve_task_18,
    "task_19": solve_task_19,
    "task_20": solve_task_20,
    "task_21": solve_task_21,
    "task_22": solve_task_22,
    "task_23": solve_task_23,
    "task_24": solve_task_24,
    "task_25": solve_task_25,
    "task_26": solve_task_26,
    "task_27": solve_task_27,
    "task_28": solve_task_28,
    "task_29": solve_task_29,
    "task_30": solve_task_30,
    "task_31": solve_task_31,
    "task_32": solve_task_32,
    "task_33": solve_task_33,
    "task_34": solve_task_34,
    "task_35": solve_task_35,
    "task_36": solve_task_36,
    "task_37": solve_task_37,
    "task_38": solve_task_38,
    "task_39": solve_task_39,
    "task_40": solve_task_40,
    "task_41": solve_task_41,
    "task_42": solve_task_42,
    "task_43": solve_task_43,
    "task_44": solve_task_44,
    "task_45": solve_task_45,
    "task_46": solve_task_46,
    "task_47": solve_task_47,
    "task_48": solve_task_48,
    "task_49": solve_task_49,
    "task_50": solve_task_50,
    "task_51": solve_task_51,
    "task_52": solve_task_52,
    "task_53": solve_task_53,
    "task_54": solve_task_54,
    "task_55": solve_task_55,
    "task_56": solve_task_56,
    "task_57": solve_task_57,
    "task_58": solve_task_58,
    "task_59": solve_task_59,
    "task_60": solve_task_60,
    "task_61": solve_task_61,
}


# ── server management ────────────────────────────────────────────────

def generate_seed_state():
    """Use Node.js to evaluate data.js and produce the seed state JSON."""
    data_js = str(APP_DIR / "js" / "data.js")
    result = subprocess.run(
        ["node", "-e", _SEED_STATE_JS, data_js],
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        raise RuntimeError(f"Failed to generate seed state:\n{result.stderr}")
    return json.loads(result.stdout)


def seed_server(server_url, seed_state):
    """PUT the seed state to the server to establish the baseline."""
    resp = requests.put(
        f"{server_url}/api/state",
        json=seed_state,
        headers={"Content-Type": "application/json"},
    )
    if resp.status_code != 200:
        raise RuntimeError(f"Failed to seed server: HTTP {resp.status_code}")


def find_free_port(start=9000):
    """Find a free port starting from `start`."""
    port = start
    while port < start + 100:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            try:
                s.bind(("", port))
                return port
            except OSError:
                port += 1
    raise RuntimeError(f"No free port found in range {start}-{start+100}")


def start_server(port):
    """Start the Figma Slides server on the given port."""
    proc = subprocess.Popen(
        [sys.executable, "server.py", "--port", str(port)],
        cwd=str(APP_DIR),
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
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
    """Stop the server process."""
    if proc and proc.poll() is None:
        proc.terminate()
        try:
            proc.wait(timeout=5)
        except subprocess.TimeoutExpired:
            proc.kill()


# ── task runner ──────────────────────────────────────────────────────

def load_tasks():
    """Load task definitions from function-tasks.json."""
    with open(TASKS_FILE) as f:
        return json.load(f)


def load_verifier(verify_path):
    """Dynamically load a verifier module."""
    full_path = APP_DIR / verify_path
    spec = importlib.util.spec_from_file_location("verifier", str(full_path))
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.verify


def run_single_task(task, server_url):
    """Reset → solve → verify for a single task."""
    task_id = task["id"]
    solver = SOLVERS.get(task_id)
    if not solver:
        return task_id, False, f"No solver defined for {task_id}"

    try:
        # 1. Reset to seed state
        resp = requests.post(f"{server_url}/api/reset")
        if resp.status_code != 200:
            return task_id, False, f"Reset failed: HTTP {resp.status_code}"

        time.sleep(0.3)

        # 2. Read seed state
        resp = requests.get(f"{server_url}/api/state")
        if resp.status_code != 200:
            return task_id, False, f"Could not read state after reset: HTTP {resp.status_code}"
        state = resp.json()

        # 3. Apply the solve function
        solver(state)

        # 4. Write solved state back
        resp = requests.put(
            f"{server_url}/api/state",
            json=state,
            headers={"Content-Type": "application/json"},
        )
        if resp.status_code != 200:
            return task_id, False, f"Could not write state: HTTP {resp.status_code}"

        # 5. Run the verifier
        verify_fn = load_verifier(task["verify"])
        passed, message = verify_fn(server_url)
        return task_id, passed, message

    except Exception as e:
        return task_id, False, f"Exception: {e}"


def run_tasks_sequential(tasks, port, seed_state):
    """Run all tasks sequentially on a single server."""
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
    """Run tasks in parallel across multiple server instances."""
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

    # Summary
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
