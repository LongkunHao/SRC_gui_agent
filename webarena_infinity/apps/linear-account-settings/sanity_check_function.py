#!/usr/bin/env python3
"""
Sanity check for Linear Account Settings function-test tasks.

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

const state = {
    _seedVersion: SEED_DATA_VERSION,
    currentUser: JSON.parse(JSON.stringify(CURRENT_USER)),
    workspaces: JSON.parse(JSON.stringify(WORKSPACES)),
    connectedAccounts: JSON.parse(JSON.stringify(CONNECTED_ACCOUNTS)),
    preferences: JSON.parse(JSON.stringify(PREFERENCES)),
    notificationSettings: JSON.parse(JSON.stringify(NOTIFICATION_SETTINGS)),
    sessions: JSON.parse(JSON.stringify(SESSIONS)),
    passkeys: JSON.parse(JSON.stringify(PASSKEYS)),
    apiKeys: JSON.parse(JSON.stringify(API_KEYS)),
    authorizedApps: JSON.parse(JSON.stringify(AUTHORIZED_APPS)),
    _nextApiKeyId: 10,
    _nextPasskeyId: 10
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


# ── solve functions ──────────────────────────────────────────────────

# Profile

def solve_task_1(state):
    """Change full name to 'Jordan Rivera'."""
    state["currentUser"]["fullName"] = "Jordan Rivera"

def solve_task_2(state):
    """Change username to 'jrivera'."""
    state["currentUser"]["username"] = "jrivera"

def solve_task_3(state):
    """Change email to 'jordan.rivera@newcorp.io'."""
    state["currentUser"]["email"] = "jordan.rivera@newcorp.io"

def solve_task_4(state):
    """Cycle avatar color from #5E6AD2 to #26B5CE."""
    state["currentUser"]["avatarColor"] = "#26B5CE"

def solve_task_5(state):
    """Disconnect GitHub."""
    state["connectedAccounts"] = [a for a in state["connectedAccounts"] if a["provider"] != "GitHub"]

def solve_task_6(state):
    """Disconnect GitLab."""
    state["connectedAccounts"] = [a for a in state["connectedAccounts"] if a["provider"] != "GitLab"]

def solve_task_7(state):
    """Disconnect Slack."""
    state["connectedAccounts"] = [a for a in state["connectedAccounts"] if a["provider"] != "Slack"]

def solve_task_8(state):
    """Disconnect Figma."""
    state["connectedAccounts"] = [a for a in state["connectedAccounts"] if a["provider"] != "Figma"]

def solve_task_9(state):
    """Disconnect Google."""
    state["connectedAccounts"] = [a for a in state["connectedAccounts"] if a["provider"] != "Google"]

def solve_task_10(state):
    """Leave 'Side Project Labs' workspace."""
    state["workspaces"] = [w for w in state["workspaces"] if w["name"] != "Side Project Labs"]

def solve_task_11(state):
    """Leave 'Open Source Collective' workspace."""
    state["workspaces"] = [w for w in state["workspaces"] if w["name"] != "Open Source Collective"]

# Preferences - Dropdowns

def solve_task_12(state):
    state["preferences"]["defaultHomeView"] = "Inbox"

def solve_task_13(state):
    state["preferences"]["defaultHomeView"] = "My Issues"

def solve_task_14(state):
    state["preferences"]["defaultHomeView"] = "Favorited Projects"

def solve_task_15(state):
    state["preferences"]["firstDayOfWeek"] = "Sunday"

def solve_task_16(state):
    state["preferences"]["firstDayOfWeek"] = "Wednesday"

def solve_task_17(state):
    state["preferences"]["interfaceTheme"] = "Dark"

def solve_task_18(state):
    state["preferences"]["interfaceTheme"] = "Light - Contrast"

def solve_task_19(state):
    state["preferences"]["fontSize"] = "Small"

def solve_task_20(state):
    state["preferences"]["fontSize"] = "Large"

def solve_task_21(state):
    state["preferences"]["gitAttachmentFormat"] = "Title and repository"

# Preferences - Toggles

def solve_task_22(state):
    state["preferences"]["displayFullNames"] = False

def solve_task_23(state):
    state["preferences"]["convertTextEmojis"] = False

def solve_task_24(state):
    state["preferences"]["usePointerCursor"] = True

def solve_task_25(state):
    state["preferences"]["openInDesktopApp"] = False

def solve_task_26(state):
    state["preferences"]["desktopNotificationBadge"] = False

def solve_task_27(state):
    state["preferences"]["enableSpellCheck"] = False

def solve_task_28(state):
    state["preferences"]["autoAssignOnCreate"] = True

def solve_task_29(state):
    state["preferences"]["autoAssignOnStarted"] = True

def solve_task_30(state):
    state["preferences"]["onGitBranchCopyMoveToStarted"] = False

def solve_task_31(state):
    state["preferences"]["onGitBranchCopyAutoAssign"] = False

# Notifications - Channel enable/disable

def solve_task_32(state):
    state["notificationSettings"]["slack"]["enabled"] = True

def solve_task_33(state):
    state["notificationSettings"]["desktop"]["enabled"] = False

def solve_task_34(state):
    state["notificationSettings"]["mobile"]["enabled"] = False

def solve_task_35(state):
    state["notificationSettings"]["email"]["enabled"] = False

# Notifications - Individual types

def solve_task_36(state):
    state["notificationSettings"]["desktop"]["cycleUpdated"] = True

def solve_task_37(state):
    state["notificationSettings"]["desktop"]["issueAssigned"] = False

def solve_task_38(state):
    state["notificationSettings"]["mobile"]["projectUpdated"] = True

def solve_task_39(state):
    state["notificationSettings"]["mobile"]["cycleUpdated"] = True

def solve_task_40(state):
    state["notificationSettings"]["email"]["issueCommented"] = True

def solve_task_41(state):
    state["notificationSettings"]["email"]["issueStatusChanged"] = False

def solve_task_42(state):
    state["notificationSettings"]["email"]["sendUrgentImmediately"] = False

def solve_task_43(state):
    state["notificationSettings"]["email"]["delayLowPriorityOutsideHours"] = False

# Notifications - Communications

def solve_task_44(state):
    state["notificationSettings"]["receiveChangelogs"] = False

def solve_task_45(state):
    state["notificationSettings"]["receiveDpaUpdates"] = False

def solve_task_46(state):
    state["notificationSettings"]["receiveProductUpdates"] = True

# Security - Sessions

def solve_task_47(state):
    state["sessions"] = [s for s in state["sessions"] if s["deviceName"] != "Safari on iPhone"]

def solve_task_48(state):
    state["sessions"] = [s for s in state["sessions"] if s["deviceName"] != "Firefox on Windows"]

def solve_task_49(state):
    state["sessions"] = [s for s in state["sessions"] if s["deviceName"] != "Chrome on Linux"]

def solve_task_50(state):
    state["sessions"] = [s for s in state["sessions"] if s.get("isCurrent", False)]

# Security - Passkeys

def solve_task_51(state):
    pk_id = state.get("_nextPasskeyId", 10)
    now = "2026-03-06T12:00:00.000Z"
    state["passkeys"].append({
        "id": f"pk_{pk_id:02d}",
        "name": "Windows Hello",
        "createdAt": now,
        "lastUsedAt": now,
        "credentialType": "platform"
    })
    state["_nextPasskeyId"] = pk_id + 1

def solve_task_52(state):
    state["passkeys"] = [p for p in state["passkeys"] if p["name"] != "YubiKey 5C NFC"]

def solve_task_53(state):
    state["passkeys"] = [p for p in state["passkeys"] if p["name"] != "iPhone Face ID"]

# Security - API Keys

def solve_task_54(state):
    key_id = state.get("_nextApiKeyId", 10)
    now = "2026-03-06T12:00:00.000Z"
    state["apiKeys"].append({
        "id": f"apikey_{key_id:02d}",
        "label": "GitHub Actions",
        "keyPrefix": "lin_api_test",
        "createdAt": now,
        "lastUsedAt": None,
        "expiresAt": None
    })
    state["_nextApiKeyId"] = key_id + 1

def solve_task_55(state):
    state["apiKeys"] = [k for k in state["apiKeys"] if k["label"] != "Mobile App Testing"]

def solve_task_56(state):
    state["apiKeys"] = [k for k in state["apiKeys"] if k["label"] != "Data Export Script"]

# Security - Authorized Apps

def solve_task_57(state):
    state["authorizedApps"] = [a for a in state["authorizedApps"] if a["name"] != "Zapier"]

def solve_task_58(state):
    state["authorizedApps"] = [a for a in state["authorizedApps"] if a["name"] != "Raycast"]

def solve_task_59(state):
    state["authorizedApps"] = [a for a in state["authorizedApps"] if a["name"] != "Linear Exporter"]

def solve_task_60(state):
    state["authorizedApps"] = [a for a in state["authorizedApps"] if a["name"] != "Marker.io"]


SOLVERS = {f"task_{i}": globals()[f"solve_task_{i}"] for i in range(1, 61)}


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
    """Start the server on the given port."""
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
    parser = argparse.ArgumentParser(description="Linear Account Settings function-task sanity check")
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
