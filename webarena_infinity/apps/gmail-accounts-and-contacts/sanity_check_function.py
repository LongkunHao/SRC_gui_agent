#!/usr/bin/env python3
"""
Sanity check for Gmail Accounts & Contacts function-test tasks.

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
    contacts: JSON.parse(JSON.stringify(CONTACTS)),
    otherContacts: JSON.parse(JSON.stringify(OTHER_CONTACTS)),
    contactLabels: JSON.parse(JSON.stringify(CONTACT_LABELS)),
    delegates: JSON.parse(JSON.stringify(DELEGATES)),
    linkedServices: JSON.parse(JSON.stringify(LINKED_SERVICES)),
    alwaysLinkedServices: JSON.parse(JSON.stringify(ALWAYS_LINKED_SERVICES)),
    accountSettings: JSON.parse(JSON.stringify(ACCOUNT_SETTINGS)),
    currentUser: JSON.parse(JSON.stringify(CURRENT_USER)),
    contactHistory: JSON.parse(JSON.stringify(CONTACT_HISTORY)),
    importExportHistory: JSON.parse(JSON.stringify(IMPORT_EXPORT_HISTORY)),
    mergeSuggestions: JSON.parse(JSON.stringify(MERGE_SUGGESTIONS)),
    _nextContactId: 50,
    _nextOtherContactId: 30,
    _nextLabelId: 20,
    _nextDelegateId: 10,
    _nextHistoryId: 20,
};
process.stdout.write(JSON.stringify(state));
"""


# ── helpers ──────────────────────────────────────────────────────────

def find_contact(state, firstName, lastName):
    for c in state["contacts"]:
        if c["firstName"] == firstName and c["lastName"] == lastName:
            return c
    raise ValueError(f"Contact not found: {firstName} {lastName}")


def find_contact_by_email(state, email):
    for c in state["contacts"]:
        if c["email"] == email:
            return c
    raise ValueError(f"Contact not found: {email}")


def find_other_contact(state, email):
    for c in state["otherContacts"]:
        if c["email"] == email:
            return c
    raise ValueError(f"Other contact not found: {email}")


def find_label(state, name):
    for l in state["contactLabels"]:
        if l["name"] == name:
            return l
    raise ValueError(f"Label not found: {name}")


def find_label_by_id(state, label_id):
    for l in state["contactLabels"]:
        if l["id"] == label_id:
            return l
    raise ValueError(f"Label not found: {label_id}")


def find_delegate(state, email):
    for d in state["delegates"]:
        if d["email"] == email:
            return d
    raise ValueError(f"Delegate not found: {email}")


def find_service(state, name):
    for s in state["linkedServices"]:
        if s["name"] == name:
            return s
    raise ValueError(f"Service not found: {name}")


def find_merge(state, merge_id):
    for m in state["mergeSuggestions"]:
        if m["id"] == merge_id:
            return m
    raise ValueError(f"Merge suggestion not found: {merge_id}")


# ── solve functions ──────────────────────────────────────────────────

def solve_task_1(state):
    """Create contact Alice Wonderland."""
    nid = state["_nextContactId"]
    state["contacts"].append({
        "id": f"contact_{nid:02d}",
        "firstName": "Alice", "lastName": "Wonderland",
        "email": "alice@wonderland.com", "phone": "", "company": "",
        "jobTitle": "", "address": "", "secondaryEmail": "",
        "secondaryPhone": "", "birthday": "", "website": "", "notes": "",
        "labels": [], "isStarred": False, "avatarColor": "#EA4335",
        "createdAt": "2026-03-07T12:00:00Z", "updatedAt": "2026-03-07T12:00:00Z",
        "source": "manual"
    })
    state["_nextContactId"] = nid + 1


def solve_task_2(state):
    """Create contact Bob Builder with full details."""
    nid = state["_nextContactId"]
    state["contacts"].append({
        "id": f"contact_{nid:02d}",
        "firstName": "Bob", "lastName": "Builder",
        "email": "bob@builder.io", "phone": "+1 (555) 123-4567",
        "company": "BuildCo", "jobTitle": "Foreman", "address": "",
        "secondaryEmail": "", "secondaryPhone": "", "birthday": "",
        "website": "", "notes": "", "labels": [], "isStarred": False,
        "avatarColor": "#EA4335",
        "createdAt": "2026-03-07T12:00:00Z", "updatedAt": "2026-03-07T12:00:00Z",
        "source": "manual"
    })
    state["_nextContactId"] = nid + 1


def solve_task_3(state):
    """Edit Sarah Chen's job title."""
    c = find_contact(state, "Sarah", "Chen")
    c["jobTitle"] = "Chief Product Officer"


def solve_task_4(state):
    """Edit Marcus Williams's company."""
    c = find_contact(state, "Marcus", "Williams")
    c["company"] = "DesignHub International"


def solve_task_5(state):
    """Edit Jake Morrison's phone."""
    c = find_contact(state, "Jake", "Morrison")
    c["phone"] = "+1 (415) 999-8888"


def solve_task_6(state):
    """Delete Tom Bradley."""
    state["contacts"] = [c for c in state["contacts"]
                         if not (c["firstName"] == "Tom" and c["lastName"] == "Bradley")]


def solve_task_7(state):
    """Delete Tony Russo."""
    state["contacts"] = [c for c in state["contacts"]
                         if not (c["firstName"] == "Tony" and c["lastName"] == "Russo")]


def solve_task_8(state):
    """Star James O'Brien."""
    c = find_contact(state, "James", "O'Brien")
    c["isStarred"] = True


def solve_task_9(state):
    """Unstar Sarah Chen."""
    c = find_contact(state, "Sarah", "Chen")
    c["isStarred"] = False


def solve_task_10(state):
    """Star David Kim."""
    c = find_contact(state, "David", "Kim")
    c["isStarred"] = True


def solve_task_11(state):
    """Edit Emily Rodriguez's notes."""
    c = find_contact(state, "Emily", "Rodriguez")
    c["notes"] = "Key investor contact for Series C round."


def solve_task_12(state):
    """Edit Priya Sharma's secondary email."""
    c = find_contact(state, "Priya", "Sharma")
    c["secondaryEmail"] = "priya.personal@outlook.com"


def solve_task_13(state):
    """Edit Dr. Patricia Nguyen's address."""
    c = find_contact(state, "Dr. Patricia", "Nguyen")
    c["address"] = "1200 California St, San Francisco, CA 94109"


def solve_task_14(state):
    """Create label 'Investors' with color '#FF5722'."""
    nid = state["_nextLabelId"]
    state["contactLabels"].append({
        "id": f"clabel_{nid}", "name": "Investors",
        "color": "#FF5722", "contactCount": 0
    })
    state["_nextLabelId"] = nid + 1


def solve_task_15(state):
    """Create label 'Conference' with default color."""
    nid = state["_nextLabelId"]
    state["contactLabels"].append({
        "id": f"clabel_{nid}", "name": "Conference",
        "color": "#757575", "contactCount": 0
    })
    state["_nextLabelId"] = nid + 1


def solve_task_16(state):
    """Rename 'Gym Buddies' to 'Fitness Friends'."""
    l = find_label(state, "Gym Buddies")
    l["name"] = "Fitness Friends"


def solve_task_17(state):
    """Delete 'Book Club' label and remove from contacts."""
    label_id = "clabel_8"
    state["contactLabels"] = [l for l in state["contactLabels"] if l["id"] != label_id]
    for c in state["contacts"]:
        c["labels"] = [lid for lid in c["labels"] if lid != label_id]


def solve_task_18(state):
    """Change Family label color to green."""
    l = find_label(state, "Family")
    l["color"] = "#34A853"


def solve_task_19(state):
    """Delete 'Travel Contacts' label and remove from contacts."""
    label_id = "clabel_11"
    state["contactLabels"] = [l for l in state["contactLabels"] if l["id"] != label_id]
    for c in state["contacts"]:
        c["labels"] = [lid for lid in c["labels"] if lid != label_id]


def solve_task_20(state):
    """Add Friends label to David Kim."""
    c = find_contact(state, "David", "Kim")
    if "clabel_2" not in c["labels"]:
        c["labels"].append("clabel_2")


def solve_task_21(state):
    """Remove Work label from Sarah Chen."""
    c = find_contact(state, "Sarah", "Chen")
    c["labels"] = [lid for lid in c["labels"] if lid != "clabel_3"]


def solve_task_22(state):
    """Add VIP Clients label to Kevin Zhao."""
    c = find_contact(state, "Kevin", "Zhao")
    if "clabel_4" not in c["labels"]:
        c["labels"].append("clabel_4")


def solve_task_23(state):
    """Remove Gym Buddies label from Chris Evans."""
    c = find_contact(state, "Chris", "Evans")
    c["labels"] = [lid for lid in c["labels"] if lid != "clabel_5"]


def solve_task_24(state):
    """Move Jason Blake from other contacts to main contacts."""
    other = find_other_contact(state, "jason.blake@salesforce.com")
    nid = state["_nextContactId"]
    state["contacts"].append({
        "id": f"contact_{nid:02d}",
        "firstName": other.get("firstName", ""), "lastName": other.get("lastName", ""),
        "email": other["email"], "phone": "", "company": "",
        "jobTitle": "", "address": "", "secondaryEmail": "",
        "secondaryPhone": "", "birthday": "", "website": "",
        "notes": "Auto-saved contact moved to main contacts.",
        "labels": [], "isStarred": False, "avatarColor": "#EA4335",
        "createdAt": "2026-03-07T12:00:00Z", "updatedAt": "2026-03-07T12:00:00Z",
        "source": "auto-promoted"
    })
    state["_nextContactId"] = nid + 1
    state["otherContacts"] = [c for c in state["otherContacts"]
                              if c["email"] != "jason.blake@salesforce.com"]


def solve_task_25(state):
    """Delete other contact Vercel Support."""
    state["otherContacts"] = [c for c in state["otherContacts"]
                              if c["email"] != "support@vercel.com"]


def solve_task_26(state):
    """Move Tina Marshall from other contacts to main contacts."""
    other = find_other_contact(state, "tina.marshall@designhub.com")
    nid = state["_nextContactId"]
    state["contacts"].append({
        "id": f"contact_{nid:02d}",
        "firstName": other.get("firstName", ""), "lastName": other.get("lastName", ""),
        "email": other["email"], "phone": "", "company": "",
        "jobTitle": "", "address": "", "secondaryEmail": "",
        "secondaryPhone": "", "birthday": "", "website": "",
        "notes": "Auto-saved contact moved to main contacts.",
        "labels": [], "isStarred": False, "avatarColor": "#EA4335",
        "createdAt": "2026-03-07T12:00:00Z", "updatedAt": "2026-03-07T12:00:00Z",
        "source": "auto-promoted"
    })
    state["_nextContactId"] = nid + 1
    state["otherContacts"] = [c for c in state["otherContacts"]
                              if c["email"] != "tina.marshall@designhub.com"]


def solve_task_27(state):
    """Delete other contact Chloe Bennett."""
    state["otherContacts"] = [c for c in state["otherContacts"]
                              if c["email"] != "chloe.b@sequoiacap.com"]


def solve_task_28(state):
    """Merge Priya Sharma + Raj Kapoor."""
    merge = find_merge(state, "merge_1")
    primary = find_contact(state, "Priya", "Sharma")
    secondary = find_contact(state, "Raj", "Kapoor")
    # Merge secondary data into primary
    if not primary["secondaryEmail"] and secondary["email"]:
        primary["secondaryEmail"] = secondary["email"]
    if not primary["secondaryPhone"] and secondary["phone"]:
        primary["secondaryPhone"] = secondary["phone"]
    for lbl in secondary["labels"]:
        if lbl not in primary["labels"]:
            primary["labels"].append(lbl)
    if secondary["notes"] and secondary["notes"] not in primary["notes"]:
        primary["notes"] = primary["notes"] + "\n" + secondary["notes"] if primary["notes"] else secondary["notes"]
    # Remove secondary contact
    state["contacts"] = [c for c in state["contacts"] if c["id"] != secondary["id"]]
    merge["dismissed"] = True


def solve_task_29(state):
    """Dismiss merge suggestion for Sophie + Elena."""
    merge = find_merge(state, "merge_2")
    merge["dismissed"] = True


def solve_task_30(state):
    """Add delegate assistant@company.com."""
    nid = state["_nextDelegateId"]
    state["delegates"].append({
        "id": f"delegate_{nid}",
        "email": "assistant@company.com",
        "name": "Office Assistant",
        "status": "pending",
        "addedAt": "2026-03-07T12:00:00Z",
        "activatedAt": None,
        "permissions": {
            "readEmail": True, "sendEmail": True, "deleteEmail": True,
            "manageChat": False, "changePassword": False
        }
    })
    state["_nextDelegateId"] = nid + 1


def solve_task_31(state):
    """Remove delegate Maya Patel."""
    state["delegates"] = [d for d in state["delegates"]
                          if d["email"] != "maya.patel@techcorp.io"]


def solve_task_32(state):
    """Remove delegate Jake Morrison."""
    state["delegates"] = [d for d in state["delegates"]
                          if d["email"] != "jake.morrison@gmail.com"]


def solve_task_33(state):
    """Remove delegate Priya Sharma."""
    state["delegates"] = [d for d in state["delegates"]
                          if d["email"] != "priya.sharma@cloudnine.dev"]


def solve_task_34(state):
    """Unlink Google Search."""
    svc = find_service(state, "Google Search")
    svc["isLinked"] = False


def solve_task_35(state):
    """Link Google Ads."""
    svc = find_service(state, "Google Ads")
    svc["isLinked"] = True


def solve_task_36(state):
    """Link Google Shopping."""
    svc = find_service(state, "Google Shopping")
    svc["isLinked"] = True


def solve_task_37(state):
    """Unlink YouTube."""
    svc = find_service(state, "YouTube")
    svc["isLinked"] = False


def solve_task_38(state):
    """Change contactsSortBy to lastName."""
    state["accountSettings"]["contactsSortBy"] = "lastName"


def solve_task_39(state):
    """Change contactsDisplayOrder to lastFirst."""
    state["accountSettings"]["contactsDisplayOrder"] = "lastFirst"


def solve_task_40(state):
    """Disable autoSaveContacts."""
    state["accountSettings"]["autoSaveContacts"] = False


def solve_task_41(state):
    """Disable shareDocsInEmail."""
    state["accountSettings"]["collaborationSettings"]["shareDocsInEmail"] = False


def solve_task_42(state):
    """Disable showContactInfo."""
    state["accountSettings"]["collaborationSettings"]["showContactInfo"] = False


def solve_task_43(state):
    """Change user name to Alexander Johnson."""
    state["currentUser"]["name"] = "Alexander Johnson"


def solve_task_44(state):
    """Change recovery email."""
    state["currentUser"]["recoveryEmail"] = "alex.new.recovery@proton.me"


def solve_task_45(state):
    """Change recovery phone."""
    state["currentUser"]["recoveryPhone"] = "+1 (415) 555-9999"


def solve_task_46(state):
    """Disable rememberPassword."""
    state["accountSettings"]["loginSettings"]["rememberPassword"] = False


def solve_task_47(state):
    """Disable autoSignIn."""
    state["accountSettings"]["loginSettings"]["autoSignIn"] = False


def solve_task_48(state):
    """Disable twoFactorEnabled."""
    state["accountSettings"]["loginSettings"]["twoFactorEnabled"] = False


def solve_task_49(state):
    """Change 2FA method to SMS."""
    state["accountSettings"]["loginSettings"]["twoFactorMethod"] = "sms"


def solve_task_50(state):
    """Change 2FA method to security_key."""
    state["accountSettings"]["loginSettings"]["twoFactorMethod"] = "security_key"


def solve_task_51(state):
    """Change showProfilePhoto to contacts_only."""
    state["accountSettings"]["privacySettings"]["showProfilePhoto"] = "contacts_only"


def solve_task_52(state):
    """Change showEmail to nobody."""
    state["accountSettings"]["privacySettings"]["showEmail"] = "nobody"


def solve_task_53(state):
    """Change showPhone to everyone."""
    state["accountSettings"]["privacySettings"]["showPhone"] = "everyone"


def solve_task_54(state):
    """Disable activityTracking."""
    state["accountSettings"]["privacySettings"]["activityTracking"] = False


def solve_task_55(state):
    """Disable delegateActivity notifications."""
    state["accountSettings"]["notificationSettings"]["delegateActivity"] = False


def solve_task_56(state):
    """Enable contactChanges notifications."""
    state["accountSettings"]["notificationSettings"]["contactChanges"] = True


def solve_task_57(state):
    """Disable securityAlerts notifications."""
    state["accountSettings"]["notificationSettings"]["securityAlerts"] = False


def solve_task_58(state):
    """Disable linkedServiceUpdates notifications."""
    state["accountSettings"]["notificationSettings"]["linkedServiceUpdates"] = False


def solve_task_59(state):
    """Disable contactsSync."""
    state["accountSettings"]["syncSettings"]["contactsSync"] = False


def solve_task_60(state):
    """Disable calendarSync."""
    state["accountSettings"]["syncSettings"]["calendarSync"] = False


def solve_task_61(state):
    """Disable emailSync."""
    state["accountSettings"]["syncSettings"]["emailSync"] = False


def solve_task_62(state):
    """Unacknowledge Google Sync deprecation."""
    state["accountSettings"]["syncSettings"]["googleSyncDeprecationAcknowledged"] = False


def solve_task_63(state):
    """Edit Ben Walker's website."""
    c = find_contact(state, "Ben", "Walker")
    c["website"] = "https://benwalker.com"


def solve_task_64(state):
    """Edit Samantha Lee's birthday."""
    c = find_contact(state, "Samantha", "Lee")
    c["birthday"] = "1993-05-20"


def solve_task_65(state):
    """Change user phone."""
    state["currentUser"]["phone"] = "+1 (650) 555-7777"


def solve_task_66(state):
    """Rename College Alumni to University Network."""
    l = find_label(state, "College Alumni")
    l["name"] = "University Network"


def solve_task_67(state):
    """Create contact Test User with Work label."""
    nid = state["_nextContactId"]
    state["contacts"].append({
        "id": f"contact_{nid:02d}",
        "firstName": "Test", "lastName": "User",
        "email": "test@example.com", "phone": "", "company": "",
        "jobTitle": "", "address": "", "secondaryEmail": "",
        "secondaryPhone": "", "birthday": "", "website": "", "notes": "",
        "labels": ["clabel_3"], "isStarred": False, "avatarColor": "#EA4335",
        "createdAt": "2026-03-07T12:00:00Z", "updatedAt": "2026-03-07T12:00:00Z",
        "source": "manual"
    })
    state["_nextContactId"] = nid + 1


def solve_task_68(state):
    """Change showProfilePhoto to nobody."""
    state["accountSettings"]["privacySettings"]["showProfilePhoto"] = "nobody"


SOLVERS = {f"task_{i}": globals()[f"solve_task_{i}"] for i in range(1, 69)}


# ── server management ────────────────────────────────────────────────

def generate_seed_state():
    """Use Node.js to evaluate data.js and produce the seed state JSON."""
    data_js = str(APP_DIR / "js" / "data.js")
    result = subprocess.run(
        ["node", "-e", _SEED_STATE_JS, data_js],
        capture_output=True, text=True,
    )
    if result.returncode != 0:
        raise RuntimeError(f"Failed to generate seed state:\n{result.stderr}")
    return json.loads(result.stdout)


def seed_server(server_url, seed_state):
    """PUT the seed state to establish the baseline."""
    resp = requests.put(
        f"{server_url}/api/state",
        json=seed_state,
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
    parser = argparse.ArgumentParser(description="Gmail Accounts & Contacts function-task sanity check")
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
