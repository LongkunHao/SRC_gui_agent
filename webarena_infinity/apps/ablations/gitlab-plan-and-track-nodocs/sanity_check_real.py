#!/usr/bin/env python3
"""Sanity check for real-task verifiers.

For each task, directly constructs the expected end-state (bypassing the agent),
then runs the verifier and asserts it returns True.
"""

import argparse
import copy
import importlib.util
import json
import os
import signal
import socket
import subprocess
import sys
import time
from concurrent.futures import ThreadPoolExecutor, as_completed

APP_DIR = os.path.dirname(os.path.abspath(__file__))
TASKS_FILE = os.path.join(APP_DIR, "real-tasks.json")
NUM_TASKS = 120


# ─── Helpers ──────────────────────────────────────────────────────────────────

def find_entity(collection, **kwargs):
    """Find a single entity by attribute match."""
    for item in collection:
        if all(item.get(k) == v for k, v in kwargs.items()):
            return item
    key_desc = ", ".join(f"{k}={v!r}" for k, v in kwargs.items())
    raise ValueError(f"Entity not found: {key_desc}")


def find_entity_by(collection, key, predicate):
    """Find entity where predicate(entity[key]) is True."""
    for item in collection:
        if predicate(item.get(key, "")):
            return item
    raise ValueError(f"No entity matched predicate on '{key}'")


def find_issue(state, issue_id):
    return find_entity(state["issues"], id=issue_id)


def find_label(state, name):
    return find_entity(state["labels"], name=name)


def find_milestone(state, title):
    return find_entity(state["milestones"], title=title)


def find_milestone_containing(state, substring):
    return find_entity_by(state["milestones"], "title", lambda t: substring in t)


def find_iteration(state, title):
    return find_entity(state["iterations"], title=title)


def find_epic(state, title):
    return find_entity(state["epics"], title=title)


def find_epic_containing(state, substring):
    return find_entity_by(state["epics"], "title", lambda t: substring in t)


def find_board(state, name):
    return find_entity(state["boards"], name=name)


def get_next_id(state, entity):
    nid = state["_nextId"][entity]
    state["_nextId"][entity] = nid + 1
    return nid


# ─── Seed State ───────────────────────────────────────────────────────────────

def generate_seed_state():
    """Extract seed state from data.js using Node."""
    js_code = r"""
    const fs = require('fs');
    const src = fs.readFileSync('%s/js/data.js', 'utf8');
    const fn = new Function(src + '; return SeedData;');
    const seed = fn();
    const state = {
        _seedVersion: seed.SEED_DATA_VERSION,
        users: JSON.parse(JSON.stringify(seed.users)),
        currentUserId: seed.currentUserId,
        labels: JSON.parse(JSON.stringify(seed.labels)),
        milestones: JSON.parse(JSON.stringify(seed.milestones)),
        iterationCadences: JSON.parse(JSON.stringify(seed.iterationCadences)),
        iterations: JSON.parse(JSON.stringify(seed.iterations)),
        epics: JSON.parse(JSON.stringify(seed.epics)),
        issueTemplates: JSON.parse(JSON.stringify(seed.issueTemplates)),
        issues: JSON.parse(JSON.stringify(seed.issues)),
        comments: JSON.parse(JSON.stringify(seed.comments)),
        activityLog: JSON.parse(JSON.stringify(seed.activityLog)),
        boards: JSON.parse(JSON.stringify(seed.boards)),
        notifications: JSON.parse(JSON.stringify(seed.notifications)),
        notificationSettings: JSON.parse(JSON.stringify(seed.notificationSettings)),
        project: JSON.parse(JSON.stringify(seed.project)),
        _nextId: JSON.parse(JSON.stringify(seed._nextId)),
    };
    process.stdout.write(JSON.stringify(state));
    """.replace('%s', APP_DIR.replace('\\', '\\\\'))

    result = subprocess.run(
        ["node", "-e", js_code],
        capture_output=True, text=True, timeout=10,
    )
    if result.returncode != 0:
        print(f"Node stderr: {result.stderr}", file=sys.stderr)
        raise RuntimeError("Failed to generate seed state from data.js")
    return json.loads(result.stdout)


# ─── Solver Functions — Easy ─────────────────────────────────────────────────

def solve_task_e1(state):
    """Close issue #33 'Memory leak in WebSocket connection handler'."""
    issue = find_issue(state, 33)
    issue["status"] = "closed"
    issue["closedAt"] = "2026-03-18T00:00:00Z"


def solve_task_e2(state):
    """Reopen issue #89 'Fix data loss on concurrent issue edits'."""
    issue = find_issue(state, 89)
    issue["status"] = "open"
    issue["closedAt"] = None


def solve_task_e3(state):
    """Set issue #14 priority to critical (swap high→critical)."""
    issue = find_issue(state, 14)
    issue["labelIds"] = [l for l in issue["labelIds"] if l != 12]
    if 11 not in issue["labelIds"]:
        issue["labelIds"].append(11)


def solve_task_e4(state):
    """Mark issue #57 as not confidential."""
    issue = find_issue(state, 57)
    issue["confidential"] = False


def solve_task_e5(state):
    """Remove Emily Okonkwo (id 8) from issue #22."""
    issue = find_issue(state, 22)
    issue["assigneeIds"] = [a for a in issue["assigneeIds"] if a != 8]


def solve_task_e6(state):
    """Set weight of issue #9 to 8."""
    issue = find_issue(state, 9)
    issue["weight"] = 8


def solve_task_e7(state):
    """Clear due date on issue #28."""
    issue = find_issue(state, 28)
    issue["dueDate"] = None


def solve_task_e8(state):
    """Add documentation label (id 3) to issue #43."""
    issue = find_issue(state, 43)
    if 3 not in issue["labelIds"]:
        issue["labelIds"].append(3)


def solve_task_e9(state):
    """Close epic 'Performance Optimization Phase 2'."""
    epic = find_epic(state, "Performance Optimization Phase 2")
    epic["status"] = "closed"


def solve_task_e10(state):
    """Reopen milestone 'v1.1 — Stability'."""
    ms = find_milestone_containing(state, "v1.1")
    ms["status"] = "active"


def solve_task_e11(state):
    """Delete the 'breaking-change' label."""
    label = find_label(state, "breaking-change")
    label_id = label["id"]
    state["labels"] = [l for l in state["labels"] if l["id"] != label_id]
    for issue in state["issues"]:
        issue["labelIds"] = [l for l in issue["labelIds"] if l != label_id]
    for epic in state["epics"]:
        epic["labels"] = [l for l in epic["labels"] if l != label_id]
    for board in state["boards"]:
        board["lists"] = [l for l in board["lists"] if l.get("labelId") != label_id]


def solve_task_e12(state):
    """Set notification level to 'watch'."""
    state["notificationSettings"]["level"] = "watch"


def solve_task_e13(state):
    """Mark all notifications as read."""
    for n in state["notifications"]:
        n["read"] = True


def solve_task_e14(state):
    """Assign Marek Kowalski (id 2) to issue #111."""
    issue = find_issue(state, 111)
    if 2 not in issue["assigneeIds"]:
        issue["assigneeIds"].append(2)


def solve_task_e15(state):
    """Remove bug label (id 1) from issue #104."""
    issue = find_issue(state, 104)
    issue["labelIds"] = [l for l in issue["labelIds"] if l != 1]


def solve_task_e16(state):
    """Move issue #55 to v2.1 Integrations milestone (id 4)."""
    issue = find_issue(state, 55)
    issue["milestoneId"] = 4


def solve_task_e17(state):
    """Set time estimate for issue #23 to 40h (144000s)."""
    issue = find_issue(state, 23)
    issue["timeEstimate"] = 144000


def solve_task_e18(state):
    """Close epic 'Accessibility Compliance (WCAG 2.1 AA)'."""
    epic = find_epic_containing(state, "Accessibility Compliance")
    epic["status"] = "closed"


def solve_task_e19(state):
    """Remove the Review list (labelId 17) from Development Board."""
    board = find_board(state, "Development Board")
    board["lists"] = [l for l in board["lists"] if l.get("labelId") != 17]
    for i, lst in enumerate(board["lists"]):
        lst["position"] = i


def solve_task_e20(state):
    """Set due date of issue #20 to 2026-05-15."""
    issue = find_issue(state, 20)
    issue["dueDate"] = "2026-05-15"


# ─── Solver Functions — Medium ───────────────────────────────────────────────

def solve_task_m1(state):
    """Create issue 'Implement GraphQL subscriptions for real-time updates'."""
    nid = get_next_id(state, "issues")
    state["issues"].append({
        "id": nid,
        "title": "Implement GraphQL subscriptions for real-time updates",
        "description": "",
        "type": "issue",
        "status": "open",
        "authorId": state["currentUserId"],
        "assigneeIds": [7],  # Li Wei
        "labelIds": [7, 2],  # backend, feature
        "milestoneId": 4,    # v2.1 — Integrations
        "iterationId": None,
        "weight": 8,
        "dueDate": None,
        "confidential": False,
        "timeEstimate": 0,
        "timeSpent": 0,
        "createdAt": "2026-03-18T00:00:00Z",
        "updatedAt": "2026-03-18T00:00:00Z",
        "closedAt": None,
        "relatedIssues": [],
    })


def solve_task_m2(state):
    """Move issue #29 from Backlog to v2.0, set priority to high."""
    issue = find_issue(state, 29)
    issue["milestoneId"] = 3  # v2.0 — API Overhaul
    issue["labelIds"] = [l for l in issue["labelIds"] if l != 13]  # remove medium
    if 12 not in issue["labelIds"]:
        issue["labelIds"].append(12)  # add high


def solve_task_m3(state):
    """Create milestone 'v2.2 — Performance'."""
    nid = get_next_id(state, "milestones")
    state["milestones"].append({
        "id": nid,
        "title": "v2.2 \u2014 Performance",
        "description": "Performance improvements and optimizations",
        "startDate": "2026-07-01",
        "dueDate": "2026-08-31",
        "status": "active",
    })


def solve_task_m4(state):
    """Create epic 'Dark Mode Support'."""
    nid = get_next_id(state, "epics")
    state["epics"].append({
        "id": nid,
        "title": "Dark Mode Support",
        "description": "Implement dark mode across all application pages",
        "status": "open",
        "startDate": None,
        "dueDate": None,
        "labels": [8, 6],  # frontend, UX
        "authorId": state["currentUserId"],
        "confidential": False,
        "childIssueIds": [],
        "childEpicIds": [],
        "createdAt": "2026-03-18T00:00:00Z",
        "updatedAt": "2026-03-18T00:00:00Z",
    })


def solve_task_m5(state):
    """Add issues #94 and #115 to Notification System Revamp epic."""
    epic = find_epic(state, "Notification System Revamp")
    for iid in [94, 115]:
        if iid not in epic["childIssueIds"]:
            epic["childIssueIds"].append(iid)


def solve_task_m6(state):
    """Create label 'regression' (#c0392b) and add to issue #35."""
    nid = get_next_id(state, "labels")
    state["labels"].append({
        "id": nid,
        "name": "regression",
        "description": "",
        "color": "#c0392b",
        "textColor": "#fff",
        "scoped": False,
    })
    issue = find_issue(state, 35)
    if nid not in issue["labelIds"]:
        issue["labelIds"].append(nid)


def solve_task_m7(state):
    """Assign David Kim (11) to issue #60, set iteration to Sprint 7 (id 7)."""
    issue = find_issue(state, 60)
    if 11 not in issue["assigneeIds"]:
        issue["assigneeIds"].append(11)
    issue["iterationId"] = 7


def solve_task_m8(state):
    """Create iteration 'Design Cycle 6' in Design Cycles cadence."""
    nid = get_next_id(state, "iterations")
    state["iterations"].append({
        "id": nid,
        "cadenceId": 2,  # Design Cycles
        "title": "Design Cycle 6",
        "startDate": "2026-06-15",
        "endDate": "2026-07-05",
        "status": "upcoming",
    })


def solve_task_m9(state):
    """Add blocks relationship from #14 to #49."""
    issue14 = find_issue(state, 14)
    issue49 = find_issue(state, 49)
    if not any(r["issueId"] == 49 for r in issue14["relatedIssues"]):
        issue14["relatedIssues"].append({"issueId": 49, "type": "blocks"})
    if not any(r["issueId"] == 14 for r in issue49["relatedIssues"]):
        issue49["relatedIssues"].append({"issueId": 14, "type": "is_blocked_by"})


def solve_task_m10(state):
    """Remove In Progress list (labelId 16), add performance list (labelId 4)."""
    board = find_board(state, "Development Board")
    board["lists"] = [l for l in board["lists"] if l.get("labelId") != 16]
    nid = get_next_id(state, "boardLists")
    closed_idx = next((i for i, l in enumerate(board["lists"]) if l["type"] == "closed"), len(board["lists"]))
    board["lists"].insert(closed_idx, {
        "id": nid,
        "type": "label",
        "title": "performance",
        "position": closed_idx,
        "labelId": 4,
    })
    for i, lst in enumerate(board["lists"]):
        lst["position"] = i


def solve_task_m11(state):
    """Close issues #57, #58, #59."""
    for issue_id in [57, 58, 59]:
        issue = find_issue(state, issue_id)
        issue["status"] = "closed"
        issue["closedAt"] = "2026-03-18T00:00:00Z"


def solve_task_m12(state):
    """Update security label color and description."""
    label = find_label(state, "security")
    label["color"] = "#8e44ad"
    label["textColor"] = "#fff"
    label["description"] = "Security vulnerabilities and hardening"


def solve_task_m13(state):
    """Add David Kim (11) to issue #42, change priority to high."""
    issue = find_issue(state, 42)
    if 11 not in issue["assigneeIds"]:
        issue["assigneeIds"].append(11)
    issue["labelIds"] = [l for l in issue["labelIds"] if l != 13]  # remove medium
    if 12 not in issue["labelIds"]:
        issue["labelIds"].append(12)  # add high


def solve_task_m14(state):
    """Set issue #2 time estimate to 60h, time spent to 10h."""
    issue = find_issue(state, 2)
    issue["timeEstimate"] = 216000  # 60h
    issue["timeSpent"] = 36000     # 10h


def solve_task_m15(state):
    """Move issue #34 to v2.1, assign Priya Sharma (5)."""
    issue = find_issue(state, 34)
    issue["milestoneId"] = 4
    if 5 not in issue["assigneeIds"]:
        issue["assigneeIds"].append(5)


def solve_task_m16(state):
    """Create confidential epic 'Security Vulnerability Assessment'."""
    nid = get_next_id(state, "epics")
    state["epics"].append({
        "id": nid,
        "title": "Security Vulnerability Assessment",
        "description": "",
        "status": "open",
        "startDate": None,
        "dueDate": None,
        "labels": [5, 11],  # security, priority::critical
        "authorId": state["currentUserId"],
        "confidential": True,
        "childIssueIds": [],
        "childEpicIds": [],
        "createdAt": "2026-03-18T00:00:00Z",
        "updatedAt": "2026-03-18T00:00:00Z",
    })


def solve_task_m17(state):
    """Add issue #74 to CI/CD epic, change milestone to v2.1."""
    epic = find_epic_containing(state, "CI/CD Pipeline")
    if 74 not in epic["childIssueIds"]:
        epic["childIssueIds"].append(74)
    issue = find_issue(state, 74)
    issue["milestoneId"] = 4


def solve_task_m18(state):
    """Update Backlog milestone description and start date."""
    ms = find_milestone(state, "Backlog")
    ms["description"] = "Items not yet scheduled for a release"
    ms["startDate"] = "2026-01-01"


def solve_task_m19(state):
    """Swap #48 out of API v3 Migration epic, add #121."""
    epic = find_epic_containing(state, "API v3 Migration")
    epic["childIssueIds"] = [i for i in epic["childIssueIds"] if i != 48]
    if 121 not in epic["childIssueIds"]:
        epic["childIssueIds"].append(121)


def solve_task_m20(state):
    """Close issue #78, add related_to link between #78 and #31."""
    issue78 = find_issue(state, 78)
    issue78["status"] = "closed"
    issue78["closedAt"] = "2026-03-18T00:00:00Z"
    issue31 = find_issue(state, 31)
    if not any(r["issueId"] == 31 for r in issue78["relatedIssues"]):
        issue78["relatedIssues"].append({"issueId": 31, "type": "related_to"})
    if not any(r["issueId"] == 78 for r in issue31["relatedIssues"]):
        issue31["relatedIssues"].append({"issueId": 78, "type": "related_to"})


# ─── Solver Functions — Hard ─────────────────────────────────────────────────

def solve_task_h1(state):
    """Create task 'API v3 rate limiting documentation' matching issue #9's assignee/milestone."""
    # Issue #9: assigneeIds [7], milestoneId 3
    nid = get_next_id(state, "issues")
    state["issues"].append({
        "id": nid,
        "title": "API v3 rate limiting documentation",
        "description": "",
        "type": "task",
        "status": "open",
        "authorId": state["currentUserId"],
        "assigneeIds": [7],  # Li Wei (same as #9)
        "labelIds": [3],     # documentation
        "milestoneId": 3,    # v2.0 (same as #9)
        "iterationId": None,
        "weight": None,
        "dueDate": None,
        "confidential": False,
        "timeEstimate": 0,
        "timeSpent": 0,
        "createdAt": "2026-03-18T00:00:00Z",
        "updatedAt": "2026-03-18T00:00:00Z",
        "closedAt": None,
        "relatedIssues": [],
    })


def solve_task_h2(state):
    """Close all open low-priority issues in v2.0 (#10, #48)."""
    for issue_id in [10, 48]:
        issue = find_issue(state, issue_id)
        issue["status"] = "closed"
        issue["closedAt"] = "2026-03-18T00:00:00Z"


def solve_task_h3(state):
    """Assign David Kim (11) to #60, #61, #62 and set iteration to Sprint 7."""
    for issue_id in [60, 61, 62]:
        issue = find_issue(state, issue_id)
        if 11 not in issue["assigneeIds"]:
            issue["assigneeIds"].append(11)
        issue["iterationId"] = 7


def solve_task_h4(state):
    """Reassign Tom's v2.1 issues to Ana Garcia."""
    for issue_id in [19, 20, 21, 42, 50, 53]:
        issue = find_issue(state, issue_id)
        issue["assigneeIds"] = [a for a in issue["assigneeIds"] if a != 6]
        if 3 not in issue["assigneeIds"]:
            issue["assigneeIds"].append(3)


def solve_task_h5(state):
    """Create 'Critical Fixes' milestone and move critical issues to it."""
    nid = get_next_id(state, "milestones")
    state["milestones"].append({
        "id": nid,
        "title": "Critical Fixes",
        "description": "",
        "startDate": None,
        "dueDate": "2026-04-01",
        "status": "active",
    })
    for issue_id in [11, 33, 41]:
        issue = find_issue(state, issue_id)
        issue["milestoneId"] = nid


def solve_task_h6(state):
    """Replace all label-based board lists with bug/feature/performance."""
    board = find_board(state, "Development Board")
    # Remove all label-based lists
    board["lists"] = [l for l in board["lists"] if l["type"] != "label"]
    # Add new label lists before the closed list
    closed_idx = next((i for i, l in enumerate(board["lists"]) if l["type"] == "closed"), len(board["lists"]))
    new_labels = [
        (1, "bug"),
        (2, "feature"),
        (4, "performance"),
    ]
    for offset, (label_id, title) in enumerate(new_labels):
        nid = get_next_id(state, "boardLists")
        board["lists"].insert(closed_idx + offset, {
            "id": nid,
            "type": "label",
            "title": title,
            "position": closed_idx + offset,
            "labelId": label_id,
        })
    for i, lst in enumerate(board["lists"]):
        lst["position"] = i


def solve_task_h7(state):
    """Close CI/CD Pipeline Modernization epic and all child issues."""
    for issue_id in [19, 20, 21, 53, 54]:
        issue = find_issue(state, issue_id)
        issue["status"] = "closed"
        issue["closedAt"] = "2026-03-18T00:00:00Z"
    epic = find_epic_containing(state, "CI/CD Pipeline Modernization")
    epic["status"] = "closed"


def solve_task_h8(state):
    """Move #47 from API v3 Migration to Perf Opt epic, change milestone and priority."""
    epic2 = find_epic_containing(state, "API v3 Migration")
    epic2["childIssueIds"] = [i for i in epic2["childIssueIds"] if i != 47]
    epic3 = find_epic(state, "Performance Optimization Phase 2")
    if 47 not in epic3["childIssueIds"]:
        epic3["childIssueIds"].append(47)
    issue = find_issue(state, 47)
    issue["milestoneId"] = 4  # v2.1
    issue["labelIds"] = [l for l in issue["labelIds"] if l != 13]  # remove medium
    if 12 not in issue["labelIds"]:
        issue["labelIds"].append(12)  # add high


def solve_task_h9(state):
    """Set Sprint 7 for Emily's open bugs without iteration (#37,#67,#72,#110,#120)."""
    for issue_id in [37, 67, 72, 110, 120]:
        issue = find_issue(state, issue_id)
        issue["iterationId"] = 7


def solve_task_h10(state):
    """Close Priya's performance issues (#11, #12, #14, #49)."""
    for issue_id in [11, 12, 14, 49]:
        issue = find_issue(state, issue_id)
        issue["status"] = "closed"
        issue["closedAt"] = "2026-03-18T00:00:00Z"


def solve_task_h11(state):
    """Create issue 'Update Redis client library to v5' matching #12's assignees/weight/milestone."""
    # Issue #12: assigneeIds [5,11], weight 13, milestoneId 3
    nid = get_next_id(state, "issues")
    state["issues"].append({
        "id": nid,
        "title": "Update Redis client library to v5",
        "description": "",
        "type": "issue",
        "status": "open",
        "authorId": state["currentUserId"],
        "assigneeIds": [5, 11],  # same as #12
        "labelIds": [7, 10, 13],  # backend, tech-debt, priority::medium
        "milestoneId": 3,         # same as #12
        "iterationId": None,
        "weight": 13,             # same as #12
        "dueDate": None,
        "confidential": False,
        "timeEstimate": 0,
        "timeSpent": 0,
        "createdAt": "2026-03-18T00:00:00Z",
        "updatedAt": "2026-03-18T00:00:00Z",
        "closedAt": None,
        "relatedIssues": [],
    })


def solve_task_h12(state):
    """Create 'blocked' label and add to migration issues #7, #8, #47."""
    nid = get_next_id(state, "labels")
    state["labels"].append({
        "id": nid,
        "name": "blocked",
        "description": "",
        "color": "#e74c3c",
        "textColor": "#fff",
        "scoped": False,
    })
    for issue_id in [7, 8, 47]:
        issue = find_issue(state, issue_id)
        if nid not in issue["labelIds"]:
            issue["labelIds"].append(nid)


def solve_task_h13(state):
    """Add blocks from #20 to #21, set both to high priority."""
    issue20 = find_issue(state, 20)
    issue21 = find_issue(state, 21)
    # Add relationship
    if not any(r["issueId"] == 21 for r in issue20["relatedIssues"]):
        issue20["relatedIssues"].append({"issueId": 21, "type": "blocks"})
    if not any(r["issueId"] == 20 for r in issue21["relatedIssues"]):
        issue21["relatedIssues"].append({"issueId": 20, "type": "is_blocked_by"})
    # Set #20 priority to high (swap medium→high)
    issue20["labelIds"] = [l for l in issue20["labelIds"] if l != 13]
    if 12 not in issue20["labelIds"]:
        issue20["labelIds"].append(12)
    # #21 already has priority::high (12)


def solve_task_h14(state):
    """Create epic 'Platform Stability' and add critical issues as children."""
    nid = get_next_id(state, "epics")
    state["epics"].append({
        "id": nid,
        "title": "Platform Stability",
        "description": "",
        "status": "open",
        "startDate": None,
        "dueDate": None,
        "labels": [4, 12],  # performance, priority::high
        "authorId": state["currentUserId"],
        "confidential": False,
        "childIssueIds": [11, 33, 41],
        "childEpicIds": [],
        "createdAt": "2026-03-18T00:00:00Z",
        "updatedAt": "2026-03-18T00:00:00Z",
    })


def solve_task_h15(state):
    """Assign Marek Kowalski (2) to unassigned security issues in v3.0 (#57,#58,#59)."""
    for issue_id in [57, 58, 59]:
        issue = find_issue(state, issue_id)
        if 2 not in issue["assigneeIds"]:
            issue["assigneeIds"].append(2)


def solve_task_h16(state):
    """Move v1.1 issues to v1.0, delete v1.1 milestone."""
    ms_v11 = find_milestone_containing(state, "v1.1")
    ms_v10 = find_milestone_containing(state, "v1.0")
    v11_id = ms_v11["id"]
    v10_id = ms_v10["id"]
    for issue in state["issues"]:
        if issue["milestoneId"] == v11_id:
            issue["milestoneId"] = v10_id
    state["milestones"] = [m for m in state["milestones"] if m["id"] != v11_id]


def solve_task_h17(state):
    """Create epic 'Q2 Bug Fixes' with v2.0 bug issues as children."""
    nid = get_next_id(state, "epics")
    state["epics"].append({
        "id": nid,
        "title": "Q2 Bug Fixes",
        "description": "",
        "status": "open",
        "startDate": None,
        "dueDate": None,
        "labels": [1, 12],  # bug, priority::high
        "authorId": state["currentUserId"],
        "confidential": False,
        "childIssueIds": [28, 31, 33, 35, 41, 78, 101, 104],
        "childEpicIds": [],
        "createdAt": "2026-03-18T00:00:00Z",
        "updatedAt": "2026-03-18T00:00:00Z",
    })


def solve_task_h18(state):
    """Add 4h time spent to Li Wei's issues with no time logged (#32,#45,#125,#129)."""
    for issue_id in [32, 45, 125, 129]:
        issue = find_issue(state, issue_id)
        issue["timeSpent"] = issue["timeSpent"] + 14400


def solve_task_h19(state):
    """Set Enterprise SSO epic and children #57,#58,#59 to not confidential."""
    epic = find_epic_containing(state, "Enterprise SSO")
    epic["confidential"] = False
    for issue_id in [57, 58, 59]:
        issue = find_issue(state, issue_id)
        issue["confidential"] = False


def solve_task_h20(state):
    """Close Notification System Revamp epic, move children to Search epic."""
    epic_notif = find_epic(state, "Notification System Revamp")
    epic_notif["status"] = "closed"
    children_to_move = [63, 64, 65]
    epic_notif["childIssueIds"] = [i for i in epic_notif["childIssueIds"] if i not in children_to_move]
    epic_search = find_epic_containing(state, "Search Infrastructure Upgrade")
    for iid in children_to_move:
        if iid not in epic_search["childIssueIds"]:
            epic_search["childIssueIds"].append(iid)


# ─── Solver Functions — Hard (Hardening Round 1) ─────────────────────────────

def solve_task_h21(state):
    """Add incident issue #41 to Perf Opt Phase 2 epic, set weight to 21."""
    epic = find_epic(state, "Performance Optimization Phase 2")
    if 41 not in epic["childIssueIds"]:
        epic["childIssueIds"].append(41)
    issue = find_issue(state, 41)
    issue["weight"] = 21


def solve_task_h22(state):
    """Close SAML issue #2 (the one in v2.0 milestone)."""
    issue = find_issue(state, 2)
    issue["status"] = "closed"
    issue["closedAt"] = "2026-03-18T00:00:00Z"


def solve_task_h23(state):
    """Create 'sprint-blocker' label and apply to critical issues in current sprint."""
    nid = get_next_id(state, "labels")
    state["labels"].append({
        "id": nid,
        "name": "sprint-blocker",
        "description": "",
        "color": "#e74c3c",
        "textColor": "#fff",
        "scoped": False,
    })
    # Current engineering sprint (cadenceId 1, status current) = Sprint 6 (id 6)
    current_sprint = next(
        it for it in state["iterations"]
        if it["cadenceId"] == 1 and it["status"] == "current"
    )
    critical_id = find_label(state, "priority::critical")["id"]
    for issue in state["issues"]:
        if (issue["status"] == "open"
                and issue.get("iterationId") == current_sprint["id"]
                and critical_id in issue.get("labelIds", [])):
            if nid not in issue["labelIds"]:
                issue["labelIds"].append(nid)


def solve_task_h24(state):
    """Add documentation label to issue #1, set due date to 2026-04-30."""
    issue = find_issue(state, 1)
    doc_id = find_label(state, "documentation")["id"]
    if doc_id not in issue["labelIds"]:
        issue["labelIds"].append(doc_id)
    issue["dueDate"] = "2026-04-30"


def solve_task_h25(state):
    """Swap status::in-progress → status::review for open Auth epic issues."""
    ip_id = find_label(state, "status::in-progress")["id"]
    rv_id = find_label(state, "status::review")["id"]
    for issue_id in [1, 3]:
        issue = find_issue(state, issue_id)
        issue["labelIds"] = [l for l in issue["labelIds"] if l != ip_id]
        if rv_id not in issue["labelIds"]:
            issue["labelIds"].append(rv_id)


def solve_task_h26(state):
    """Close bugs #28, #31, #78, #101, #104."""
    for issue_id in [28, 31, 78, 101, 104]:
        issue = find_issue(state, issue_id)
        issue["status"] = "closed"
        issue["closedAt"] = "2026-03-18T00:00:00Z"


def solve_task_h27(state):
    """Move #60, #61, #62 to v2.0 milestone and set priority to high."""
    v2_id = find_milestone_containing(state, "v2.0")["id"]
    high_id = find_label(state, "priority::high")["id"]
    priority_ids = [
        l["id"] for l in state["labels"]
        if l["name"].startswith("priority::") and l["id"] != high_id
    ]
    for issue_id in [60, 61, 62]:
        issue = find_issue(state, issue_id)
        issue["milestoneId"] = v2_id
        issue["labelIds"] = [l for l in issue["labelIds"] if l not in priority_ids]
        if high_id not in issue["labelIds"]:
            issue["labelIds"].append(high_id)


def solve_task_h28(state):
    """Assign Ana Garcia (3) to open children of Perf Opt Phase 2 epic."""
    epic = find_epic(state, "Performance Optimization Phase 2")
    author_id = epic["authorId"]  # 3 = Ana Garcia
    for issue_id in [11, 12, 14, 49, 50]:
        issue = find_issue(state, issue_id)
        if author_id not in issue["assigneeIds"]:
            issue["assigneeIds"].append(author_id)


def solve_task_h29(state):
    """Create 'Security Hardening' milestone, move open confidential issues."""
    nid = get_next_id(state, "milestones")
    state["milestones"].append({
        "id": nid,
        "title": "Security Hardening",
        "description": "",
        "startDate": "2026-04-01",
        "dueDate": "2026-05-31",
        "status": "active",
    })
    for issue in state["issues"]:
        if issue.get("confidential") and issue["status"] == "open":
            issue["milestoneId"] = nid


def solve_task_h30(state):
    """Swap status::to-do → status::in-progress for #2 and #23."""
    todo_id = find_label(state, "status::to-do")["id"]
    ip_id = find_label(state, "status::in-progress")["id"]
    for issue_id in [2, 23]:
        issue = find_issue(state, issue_id)
        issue["labelIds"] = [l for l in issue["labelIds"] if l != todo_id]
        if ip_id not in issue["labelIds"]:
            issue["labelIds"].append(ip_id)


def solve_task_h31(state):
    """Match #60 to CDN issue #13: assign Tom (6), weight 5, Sprint 7, add performance."""
    issue = find_issue(state, 60)
    if 6 not in issue["assigneeIds"]:
        issue["assigneeIds"].append(6)
    issue["weight"] = 5
    sprint7 = find_iteration(state, "Sprint 7")
    issue["iterationId"] = sprint7["id"]
    perf_id = find_label(state, "performance")["id"]
    if perf_id not in issue["labelIds"]:
        issue["labelIds"].append(perf_id)


def solve_task_h32(state):
    """Move #88, #89 to v1.0, delete v1.2 Hotfixes milestone."""
    v10 = find_milestone_containing(state, "v1.0")
    v12 = find_milestone_containing(state, "v1.2")
    v12_id = v12["id"]
    v10_id = v10["id"]
    for issue in state["issues"]:
        if issue["milestoneId"] == v12_id:
            issue["milestoneId"] = v10_id
    state["milestones"] = [m for m in state["milestones"] if m["id"] != v12_id]


def solve_task_h33(state):
    """Add Backlog feature+backend unassigned issues to Search Infrastructure epic."""
    epic = find_epic_containing(state, "Search Infrastructure Upgrade")
    backlog = find_milestone(state, "Backlog")
    feature_id = find_label(state, "feature")["id"]
    backend_id = find_label(state, "backend")["id"]
    for issue in state["issues"]:
        if (issue["status"] == "open"
                and issue.get("milestoneId") == backlog["id"]
                and feature_id in issue.get("labelIds", [])
                and backend_id in issue.get("labelIds", [])
                and not issue.get("assigneeIds")):
            if issue["id"] not in epic["childIssueIds"]:
                epic["childIssueIds"].append(issue["id"])


def solve_task_h34(state):
    """Set timeEstimate to 72000 (20h) for API v3 Migration open children with no time spent."""
    for issue_id in [8, 10, 47, 48]:
        issue = find_issue(state, issue_id)
        issue["timeEstimate"] = 72000


def solve_task_h35(state):
    """Replace Jun (4) with Ana (3) on open Auth epic issues #1, #2, #46."""
    for issue_id in [1, 2, 46]:
        issue = find_issue(state, issue_id)
        issue["assigneeIds"] = [a for a in issue["assigneeIds"] if a != 4]
        if 3 not in issue["assigneeIds"]:
            issue["assigneeIds"].append(3)


def solve_task_h36(state):
    """Add blocks from #14 to #41, set both to priority::critical."""
    issue14 = find_issue(state, 14)
    issue41 = find_issue(state, 41)
    if not any(r["issueId"] == 41 for r in issue14["relatedIssues"]):
        issue14["relatedIssues"].append({"issueId": 41, "type": "blocks"})
    if not any(r["issueId"] == 14 for r in issue41["relatedIssues"]):
        issue41["relatedIssues"].append({"issueId": 14, "type": "is_blocked_by"})
    # Set #14 to critical (swap high→critical)
    crit_id = find_label(state, "priority::critical")["id"]
    high_id = find_label(state, "priority::high")["id"]
    issue14["labelIds"] = [l for l in issue14["labelIds"] if l != high_id]
    if crit_id not in issue14["labelIds"]:
        issue14["labelIds"].append(crit_id)
    # #41 already has critical


def solve_task_h37(state):
    """Log 8h time spent on Tom's high-priority v2.1 issues #19, #21, #53."""
    for issue_id in [19, 21, 53]:
        issue = find_issue(state, issue_id)
        issue["timeSpent"] = issue["timeSpent"] + 28800


def solve_task_h38(state):
    """Create epic 'Technical Debt Cleanup' with tech-debt children."""
    nid = get_next_id(state, "epics")
    tech_debt_id = find_label(state, "tech-debt")["id"]
    medium_id = find_label(state, "priority::medium")["id"]
    children = [
        i["id"] for i in state["issues"]
        if i["status"] == "open" and tech_debt_id in i.get("labelIds", [])
    ]
    state["epics"].append({
        "id": nid,
        "title": "Technical Debt Cleanup",
        "description": "",
        "status": "open",
        "startDate": None,
        "dueDate": None,
        "labels": [tech_debt_id, medium_id],
        "authorId": state["currentUserId"],
        "confidential": False,
        "childIssueIds": children,
        "childEpicIds": [],
        "createdAt": "2026-03-18T00:00:00Z",
        "updatedAt": "2026-03-18T00:00:00Z",
    })


def solve_task_h39(state):
    """Add David Kim (11) to breaking-change issues #7 and #47 in v2.0."""
    for issue_id in [7, 47]:
        issue = find_issue(state, issue_id)
        if 11 not in issue["assigneeIds"]:
            issue["assigneeIds"].append(11)


def solve_task_h40(state):
    """Close Perf Opt Phase 2 epic, set children to low priority + Backlog."""
    epic = find_epic(state, "Performance Optimization Phase 2")
    epic["status"] = "closed"
    low_id = find_label(state, "priority::low")["id"]
    priority_ids = [
        l["id"] for l in state["labels"]
        if l["name"].startswith("priority::") and l["id"] != low_id
    ]
    backlog = find_milestone(state, "Backlog")
    for issue_id in [11, 12, 14, 49, 50]:
        issue = find_issue(state, issue_id)
        issue["milestoneId"] = backlog["id"]
        issue["labelIds"] = [l for l in issue["labelIds"] if l not in priority_ids]
        if low_id not in issue["labelIds"]:
            issue["labelIds"].append(low_id)


# ─── Solver Functions — Hard (Hardening Round 2) ─────────────────────────────

def solve_task_h41(state):
    """Remove closed children from Marek's largest epic, set dueDate to 2026-06-30."""
    # Marek (2) authored epic 2 (7 children) and epic 9 (3 children).
    epic = find_entity(state["epics"], id=2)
    closed_ids = [
        i["id"] for i in state["issues"]
        if i["id"] in epic["childIssueIds"] and i["status"] == "closed"
    ]
    epic["childIssueIds"] = [c for c in epic["childIssueIds"] if c not in closed_ids]
    epic["dueDate"] = "2026-06-30"


def solve_task_h42(state):
    """Assign Notification System Revamp author (Priya, 5) to children, add to-do."""
    epic = find_epic(state, "Notification System Revamp")
    author_id = epic["authorId"]  # 5
    todo_id = find_label(state, "status::to-do")["id"]
    for issue_id in epic["childIssueIds"]:
        issue = find_issue(state, issue_id)
        if issue["status"] != "open":
            continue
        if author_id not in issue["assigneeIds"]:
            issue["assigneeIds"].append(author_id)
        if todo_id not in issue["labelIds"]:
            issue["labelIds"].append(todo_id)


def solve_task_h43(state):
    """Add devops label, Priya (5), and v2.0 milestone to issue #61."""
    issue = find_issue(state, 61)
    devops_id = find_label(state, "devops")["id"]
    if devops_id not in issue["labelIds"]:
        issue["labelIds"].append(devops_id)
    if 5 not in issue["assigneeIds"]:
        issue["assigneeIds"].append(5)
    issue["milestoneId"] = find_milestone_containing(state, "v2.0")["id"]


def solve_task_h44(state):
    """Set timeEstimate to 86400 (24h) for open breaking-change v2.0 issues with no time spent."""
    bc_id = find_label(state, "breaking-change")["id"]
    v2_id = find_milestone_containing(state, "v2.0")["id"]
    for issue in state["issues"]:
        if (issue["status"] == "open"
                and issue.get("milestoneId") == v2_id
                and bc_id in issue.get("labelIds", [])
                and issue.get("timeSpent", 0) == 0):
            issue["timeEstimate"] = 86400


def solve_task_h45(state):
    """Create Sprint 9, move devops Sprint 8 issues into it."""
    nid = get_next_id(state, "iterations")
    state["iterations"].append({
        "id": nid,
        "cadenceId": 1,
        "title": "Sprint 9",
        "startDate": "2026-04-28",
        "endDate": "2026-05-11",
        "status": "upcoming",
    })
    devops_id = find_label(state, "devops")["id"]
    sprint8 = find_iteration(state, "Sprint 8")
    for issue in state["issues"]:
        if (issue["status"] == "open"
                and issue.get("iterationId") == sprint8["id"]
                and devops_id in issue.get("labelIds", [])):
            issue["iterationId"] = nid


def solve_task_h46(state):
    """Set related issue #33 to match incident #41 weight and assignees."""
    incident = next(i for i in state["issues"] if i.get("type") == "incident")
    related_id = incident["relatedIssues"][0]["issueId"]  # 33
    related = find_issue(state, related_id)
    related["weight"] = incident["weight"]
    for aid in incident["assigneeIds"]:
        if aid not in related["assigneeIds"]:
            related["assigneeIds"].append(aid)


def solve_task_h47(state):
    """Close medium-priority children of Mobile Responsive epic, remove from epic."""
    epic = find_epic_containing(state, "Mobile Responsive Redesign")
    medium_id = find_label(state, "priority::medium")["id"]
    to_remove = []
    for issue_id in list(epic["childIssueIds"]):
        issue = find_issue(state, issue_id)
        if issue["status"] == "open" and medium_id in issue.get("labelIds", []):
            issue["status"] = "closed"
            issue["closedAt"] = "2026-03-18T00:00:00Z"
            to_remove.append(issue_id)
    epic["childIssueIds"] = [c for c in epic["childIssueIds"] if c not in to_remove]


def solve_task_h48(state):
    """Add open security+backend issues as children of Enterprise SSO epic."""
    epic = find_epic_containing(state, "Enterprise SSO")
    sec_id = find_label(state, "security")["id"]
    be_id = find_label(state, "backend")["id"]
    for issue in state["issues"]:
        if (issue["status"] == "open"
                and sec_id in issue.get("labelIds", [])
                and be_id in issue.get("labelIds", [])
                and issue["id"] not in epic["childIssueIds"]):
            epic["childIssueIds"].append(issue["id"])


def solve_task_h49(state):
    """Create 'needs-review' label, apply to to-do issues in API v3 Migration epic."""
    nid = get_next_id(state, "labels")
    state["labels"].append({
        "id": nid,
        "name": "needs-review",
        "description": "",
        "color": "#3498db",
        "textColor": "#fff",
        "scoped": False,
    })
    epic = find_epic_containing(state, "API v3 Migration")
    todo_id = find_label(state, "status::to-do")["id"]
    for issue_id in epic["childIssueIds"]:
        issue = find_issue(state, issue_id)
        if issue["status"] == "open" and todo_id in issue.get("labelIds", []):
            if nid not in issue["labelIds"]:
                issue["labelIds"].append(nid)


def solve_task_h50(state):
    """Set high-priority v2.1 issues to in-progress, low-priority to to-do."""
    v21_id = find_milestone_containing(state, "v2.1")["id"]
    high_id = find_label(state, "priority::high")["id"]
    low_id = find_label(state, "priority::low")["id"]
    ip_id = find_label(state, "status::in-progress")["id"]
    todo_id = find_label(state, "status::to-do")["id"]
    status_ids = [l["id"] for l in state["labels"] if l["name"].startswith("status::")]
    for issue in state["issues"]:
        if issue["status"] != "open" or issue.get("milestoneId") != v21_id:
            continue
        if high_id in issue.get("labelIds", []):
            issue["labelIds"] = [l for l in issue["labelIds"] if l not in status_ids]
            issue["labelIds"].append(ip_id)
        elif low_id in issue.get("labelIds", []):
            issue["labelIds"] = [l for l in issue["labelIds"] if l not in status_ids]
            issue["labelIds"].append(todo_id)


def solve_task_h51(state):
    """Close highest-weight Sprint 6 issue (#41) after logging remaining time."""
    issue = find_issue(state, 41)
    remaining = issue["timeEstimate"] - issue["timeSpent"]
    if remaining > 0:
        issue["timeSpent"] += remaining
    issue["status"] = "closed"
    issue["closedAt"] = "2026-03-18T00:00:00Z"


def solve_task_h52(state):
    """Assign Karl Fischer (9) to unassigned open security issues #57, #58, #59."""
    karl_id = 9
    sec_id = find_label(state, "security")["id"]
    for issue in state["issues"]:
        if (issue["status"] == "open"
                and sec_id in issue.get("labelIds", [])
                and not issue.get("assigneeIds")):
            if karl_id not in issue["assigneeIds"]:
                issue["assigneeIds"].append(karl_id)


def solve_task_h53(state):
    """Swap UX for needs-investigation on open Accessibility epic children with frontend+UX."""
    ux_id = find_label(state, "UX")["id"]
    ni_id = find_label(state, "needs-investigation")["id"]
    fe_id = find_label(state, "frontend")["id"]
    epic = find_epic_containing(state, "Accessibility Compliance")
    for issue_id in epic["childIssueIds"]:
        issue = find_issue(state, issue_id)
        if (issue["status"] == "open"
                and fe_id in issue.get("labelIds", [])
                and ux_id in issue.get("labelIds", [])):
            issue["labelIds"] = [l for l in issue["labelIds"] if l != ux_id]
            if ni_id not in issue["labelIds"]:
                issue["labelIds"].append(ni_id)


def solve_task_h54(state):
    """Move open devops v3.0 issues (#54, #108) to v2.1, set priority to medium."""
    v21_id = find_milestone_containing(state, "v2.1")["id"]
    med_id = find_label(state, "priority::medium")["id"]
    priority_ids = [
        l["id"] for l in state["labels"]
        if l["name"].startswith("priority::") and l["id"] != med_id
    ]
    for issue_id in [54, 108]:
        issue = find_issue(state, issue_id)
        issue["milestoneId"] = v21_id
        issue["labelIds"] = [l for l in issue["labelIds"] if l not in priority_ids]
        if med_id not in issue["labelIds"]:
            issue["labelIds"].append(med_id)


def solve_task_h55(state):
    """Move Sprint 8 issues to Sprint 7, delete Sprint 8."""
    s7 = find_iteration(state, "Sprint 7")
    s8 = find_iteration(state, "Sprint 8")
    s8_id = s8["id"]
    s7_id = s7["id"]
    for issue in state["issues"]:
        if issue.get("iterationId") == s8_id:
            issue["iterationId"] = s7_id
    state["iterations"] = [it for it in state["iterations"] if it["id"] != s8_id]


def solve_task_h56(state):
    """Add needs-investigation to all open issues with is_blocked_by relationships."""
    ni_id = find_label(state, "needs-investigation")["id"]
    for issue in state["issues"]:
        if issue["status"] != "open":
            continue
        for rel in issue.get("relatedIssues", []):
            if rel.get("type") == "is_blocked_by":
                if ni_id not in issue["labelIds"]:
                    issue["labelIds"].append(ni_id)
                break


def solve_task_h57(state):
    """Create 'Frontend Modernization' epic with unassigned Backlog frontend issues."""
    nid = get_next_id(state, "epics")
    fe_id = find_label(state, "frontend")["id"]
    ux_id = find_label(state, "UX")["id"]
    backlog = find_milestone(state, "Backlog")
    children = [
        i["id"] for i in state["issues"]
        if (i["status"] == "open"
            and i.get("milestoneId") == backlog["id"]
            and fe_id in i.get("labelIds", [])
            and not i.get("assigneeIds"))
    ]
    state["epics"].append({
        "id": nid,
        "title": "Frontend Modernization",
        "description": "",
        "status": "open",
        "startDate": None,
        "dueDate": None,
        "labels": [fe_id, ux_id],
        "authorId": state["currentUserId"],
        "confidential": False,
        "childIssueIds": children,
        "childEpicIds": [],
        "createdAt": "2026-03-18T00:00:00Z",
        "updatedAt": "2026-03-18T00:00:00Z",
    })


def solve_task_h58(state):
    """Reopen closed epic 7 (Data Export), assign David Kim (11) to children."""
    epic = find_epic(state, "Data Export & Reporting")
    epic["status"] = "open"
    for issue_id in epic["childIssueIds"]:
        issue = find_issue(state, issue_id)
        if 11 not in issue["assigneeIds"]:
            issue["assigneeIds"].append(11)


def solve_task_h59(state):
    """Make open Auth Overhaul children confidential, set epic startDate."""
    epic = find_epic_containing(state, "User Authentication Overhaul")
    epic["startDate"] = "2026-03-01"
    for issue_id in epic["childIssueIds"]:
        issue = find_issue(state, issue_id)
        if issue["status"] == "open":
            issue["confidential"] = True


def solve_task_h60(state):
    """Set current Design Cycle (id 12) and weight 5 for open Accessibility epic children."""
    dc4 = next(
        it for it in state["iterations"]
        if it["cadenceId"] == 2 and it["status"] == "current"
    )
    epic = find_epic_containing(state, "Accessibility Compliance")
    for issue_id in epic["childIssueIds"]:
        issue = find_issue(state, issue_id)
        if issue["status"] == "open":
            issue["iterationId"] = dc4["id"]
            issue["weight"] = 5


# ─── Hardening Round 3 Solvers (h61–h80) ────────────────────────────────────


def solve_task_h61(state):
    """Assign most-commenting user (Priya, 5) to open Auth Overhaul children."""
    priya_id = 5
    epic = find_epic_containing(state, "User Authentication Overhaul")
    for issue_id in epic["childIssueIds"]:
        issue = find_issue(state, issue_id)
        if issue["status"] == "open" and priya_id not in issue["assigneeIds"]:
            issue["assigneeIds"].append(priya_id)


def solve_task_h62(state):
    """Close newer performance epic (9), merge children into older epic (3)."""
    epic9 = find_entity(state["epics"], id=9)
    epic3 = find_entity(state["epics"], id=3)
    epic9["status"] = "closed"
    for cid in epic9["childIssueIds"]:
        if cid not in epic3["childIssueIds"]:
            epic3["childIssueIds"].append(cid)
    epic9["childIssueIds"] = []


def solve_task_h63(state):
    """Set bug issues to critical and feature issues to low in v2.0."""
    bug_id = find_label(state, "bug")["id"]
    feature_id = find_label(state, "feature")["id"]
    critical_id = find_label(state, "priority::critical")["id"]
    low_id = find_label(state, "priority::low")["id"]
    priority_ids = [
        l["id"] for l in state["labels"] if l["name"].startswith("priority::")
    ]
    v20_id = find_milestone_containing(state, "v2.0")["id"]
    for issue in state["issues"]:
        if issue["status"] != "open" or issue.get("milestoneId") != v20_id:
            continue
        if bug_id in issue.get("labelIds", []):
            issue["labelIds"] = [l for l in issue["labelIds"] if l not in priority_ids]
            if critical_id not in issue["labelIds"]:
                issue["labelIds"].append(critical_id)
        elif feature_id in issue.get("labelIds", []):
            issue["labelIds"] = [l for l in issue["labelIds"] if l not in priority_ids]
            if low_id not in issue["labelIds"]:
                issue["labelIds"].append(low_id)


def solve_task_h64(state):
    """Move breaking-change children of API v3 epic to v2.1, strip label."""
    bc_id = find_label(state, "breaking-change")["id"]
    v21_id = find_milestone_containing(state, "v2.1")["id"]
    epic = find_epic_containing(state, "API v3 Migration")
    for issue_id in epic["childIssueIds"]:
        issue = find_issue(state, issue_id)
        if issue["status"] == "open" and bc_id in issue.get("labelIds", []):
            issue["milestoneId"] = v21_id
            issue["labelIds"] = [l for l in issue["labelIds"] if l != bc_id]


def solve_task_h65(state):
    """Assign Priya (5, most in Sprint 6) to unassigned open priority::high issues."""
    priya_id = 5
    high_id = find_label(state, "priority::high")["id"]
    for issue in state["issues"]:
        if (issue["status"] == "open"
                and high_id in issue.get("labelIds", [])
                and not issue.get("assigneeIds")):
            issue["assigneeIds"].append(priya_id)


def solve_task_h66(state):
    """Set time estimate = 2*weight hours, time spent = half estimate for CI/CD children."""
    epic = find_epic_containing(state, "CI/CD Pipeline Modernization")
    for issue_id in epic["childIssueIds"]:
        issue = find_issue(state, issue_id)
        if issue["status"] == "open":
            est = issue["weight"] * 2 * 3600
            issue["timeEstimate"] = est
            issue["timeSpent"] = est // 2


def solve_task_h67(state):
    """Create 'stale' label, apply to unassigned low-weight Backlog issues."""
    nid = get_next_id(state, "labels")
    state["labels"].append({
        "id": nid,
        "name": "stale",
        "description": "Stale issue",
        "color": "#95a5a6",
        "textColor": "#fff",
        "scoped": False,
    })
    backlog_id = find_milestone(state, "Backlog")["id"]
    for issue in state["issues"]:
        if (issue["status"] == "open"
                and issue.get("milestoneId") == backlog_id
                and not issue.get("assigneeIds")
                and (issue.get("weight") or 0) <= 3):
            if nid not in issue["labelIds"]:
                issue["labelIds"].append(nid)


def solve_task_h68(state):
    """Close Emily's (8) open Backlog issues and set weight to 1."""
    emily_id = 8
    backlog_id = find_milestone(state, "Backlog")["id"]
    for issue in state["issues"]:
        if (issue["status"] == "open"
                and issue.get("milestoneId") == backlog_id
                and emily_id in issue.get("assigneeIds", [])):
            issue["status"] = "closed"
            issue["closedAt"] = "2026-03-18T00:00:00Z"
            issue["weight"] = 1


def solve_task_h69(state):
    """Copy blocker (#1) assignees and weight to issue #2."""
    issue2 = find_issue(state, 2)
    issue1 = find_issue(state, 1)
    for uid in issue1["assigneeIds"]:
        if uid not in issue2["assigneeIds"]:
            issue2["assigneeIds"].append(uid)
    issue2["weight"] = issue1["weight"]


def solve_task_h70(state):
    """Log 25% of time estimate for Sprint 7 issues with no time spent."""
    s7 = find_iteration(state, "Sprint 7")
    for issue in state["issues"]:
        if (issue["status"] == "open"
                and issue.get("iterationId") == s7["id"]
                and issue.get("timeEstimate", 0) > 0
                and issue.get("timeSpent", 0) == 0):
            issue["timeSpent"] = issue["timeEstimate"] // 4


def solve_task_h71(state):
    """Move SSO epic children to Auth Overhaul epic, change milestone to v2.0."""
    epic8 = find_epic_containing(state, "Enterprise SSO Integration")
    epic1 = find_epic_containing(state, "User Authentication Overhaul")
    v20_id = find_milestone_containing(state, "v2.0")["id"]
    children = list(epic8["childIssueIds"])
    epic8["childIssueIds"] = []
    for cid in children:
        if cid not in epic1["childIssueIds"]:
            epic1["childIssueIds"].append(cid)
        issue = find_issue(state, cid)
        issue["milestoneId"] = v20_id


def solve_task_h72(state):
    """Set #15 (co-assigned Jun+Emily, in epic) to critical priority and 40h estimate."""
    issue = find_issue(state, 15)
    critical_id = find_label(state, "priority::critical")["id"]
    priority_ids = [
        l["id"] for l in state["labels"] if l["name"].startswith("priority::")
    ]
    issue["labelIds"] = [l for l in issue["labelIds"] if l not in priority_ids]
    issue["labelIds"].append(critical_id)
    issue["timeEstimate"] = 144000


def solve_task_h73(state):
    """Add blocks from #32 to #36, set #36 weight to sum."""
    issue32 = find_issue(state, 32)
    issue36 = find_issue(state, 36)
    issue32["relatedIssues"].append({"issueId": 36, "type": "blocks"})
    issue36["relatedIssues"].append({"issueId": 32, "type": "is_blocked_by"})
    issue36["weight"] = issue32["weight"] + issue36["weight"]


def solve_task_h74(state):
    """Change to-do → in-progress for API v3 Migration epic (highest weight) children."""
    todo_id = find_label(state, "status::to-do")["id"]
    ip_id = find_label(state, "status::in-progress")["id"]
    epic = find_epic_containing(state, "API v3 Migration")
    for issue_id in epic["childIssueIds"]:
        issue = find_issue(state, issue_id)
        if issue["status"] == "open" and todo_id in issue.get("labelIds", []):
            issue["labelIds"] = [l for l in issue["labelIds"] if l != todo_id]
            if ip_id not in issue["labelIds"]:
                issue["labelIds"].append(ip_id)


def solve_task_h75(state):
    """Close weight-1 Backlog issues and clear assignees."""
    backlog_id = find_milestone(state, "Backlog")["id"]
    for issue in state["issues"]:
        if (issue["status"] == "open"
                and issue.get("milestoneId") == backlog_id
                and issue.get("weight") == 1):
            issue["status"] = "closed"
            issue["closedAt"] = "2026-03-18T00:00:00Z"
            issue["assigneeIds"] = []


def solve_task_h76(state):
    """Set due dates on Mobile epic children and extend epic due date."""
    epic = find_epic_containing(state, "Mobile Responsive Redesign")
    for issue_id in epic["childIssueIds"]:
        issue = find_issue(state, issue_id)
        if issue["status"] == "open":
            issue["dueDate"] = "2026-06-30"
    epic["dueDate"] = "2026-07-31"


def solve_task_h77(state):
    """Extend Auth Overhaul epic due +30d, set priority::high for unlogged children."""
    epic = find_epic_containing(state, "User Authentication Overhaul")
    epic["dueDate"] = "2026-05-30"
    high_id = find_label(state, "priority::high")["id"]
    priority_ids = [
        l["id"] for l in state["labels"] if l["name"].startswith("priority::")
    ]
    for issue_id in epic["childIssueIds"]:
        issue = find_issue(state, issue_id)
        if issue["status"] == "open" and issue.get("timeSpent", 0) == 0:
            issue["labelIds"] = [l for l in issue["labelIds"] if l not in priority_ids]
            if high_id not in issue["labelIds"]:
                issue["labelIds"].append(high_id)


def solve_task_h78(state):
    """Assign Sarah (1) and needs-investigation to all open v3.0 issues."""
    sarah_id = 1
    ni_id = find_label(state, "needs-investigation")["id"]
    v30_id = find_milestone_containing(state, "v3.0")["id"]
    for issue in state["issues"]:
        if issue["status"] == "open" and issue.get("milestoneId") == v30_id:
            if sarah_id not in issue["assigneeIds"]:
                issue["assigneeIds"].append(sarah_id)
            if ni_id not in issue["labelIds"]:
                issue["labelIds"].append(ni_id)


def solve_task_h79(state):
    """Move frontend Sprint 6 issues to Sprint 7."""
    fe_id = find_label(state, "frontend")["id"]
    s6 = find_iteration(state, "Sprint 6")
    s7 = find_iteration(state, "Sprint 7")
    for issue in state["issues"]:
        if (issue["status"] == "open"
                and issue.get("iterationId") == s6["id"]
                and fe_id in issue.get("labelIds", [])):
            issue["iterationId"] = s7["id"]


def solve_task_h80(state):
    """Assign Ana Garcia (3) to confidential epic (8) children, set start date."""
    ana_id = 3
    epic = find_entity(state["epics"], id=8)
    epic["startDate"] = "2026-04-01"
    for issue_id in epic["childIssueIds"]:
        issue = find_issue(state, issue_id)
        if ana_id not in issue["assigneeIds"]:
            issue["assigneeIds"].append(ana_id)


# ─── Solver Registry ──────────────────────────────────────────────────────────

SOLVERS = {}
for _difficulty, _prefix, _count in [("easy", "e", 20), ("medium", "m", 20), ("hard", "h", 80)]:
    for _i in range(1, _count + 1):
        _task_id = f"task_{_prefix}{_i}"
        _fn_name = f"solve_task_{_prefix}{_i}"
        SOLVERS[_task_id] = globals()[_fn_name]


# ─── Server Management ───────────────────────────────────────────────────────

def find_free_port(start=9200):
    for port in range(start, start + 200):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            try:
                s.bind(("", port))
                return port
            except OSError:
                continue
    raise RuntimeError(f"No free port found starting from {start}")


def kill_port(port):
    """Kill any process on the given port."""
    try:
        result = subprocess.run(
            ["lsof", "-ti", f":{port}"], capture_output=True, text=True
        )
        if result.stdout.strip():
            for pid in result.stdout.strip().split("\n"):
                try:
                    os.kill(int(pid), signal.SIGKILL)
                except (ProcessLookupError, ValueError):
                    pass
            time.sleep(0.3)
    except FileNotFoundError:
        pass


def start_server(port, seed_state):
    """Start the app server and PUT seed state."""
    import requests

    kill_port(port)
    proc = subprocess.Popen(
        [sys.executable, "server.py", "--port", str(port)],
        cwd=APP_DIR,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )

    # Wait for server
    url = f"http://localhost:{port}"
    for _ in range(30):
        try:
            requests.get(f"{url}/index.html", timeout=1)
            break
        except Exception:
            time.sleep(0.2)
    else:
        proc.kill()
        raise RuntimeError(f"Server on port {port} did not start")

    # PUT seed state
    resp = requests.put(
        f"{url}/api/state",
        json=seed_state,
        headers={"Content-Type": "application/json"},
        timeout=5,
    )
    if resp.status_code != 200:
        proc.kill()
        raise RuntimeError(f"Failed to PUT seed state: {resp.status_code}")

    return proc, url


def stop_server(proc):
    if proc:
        proc.terminate()
        try:
            proc.wait(timeout=5)
        except subprocess.TimeoutExpired:
            proc.kill()


# ─── Task Execution ──────────────────────────────────────────────────────────

def load_verifier(verify_path):
    """Dynamically load a verifier module."""
    full_path = os.path.join(APP_DIR, verify_path)
    spec = importlib.util.spec_from_file_location("verifier", full_path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod.verify


def run_single_task(task, port, seed_state):
    """Reset → solve → verify for a single task."""
    import requests

    task_id = task["id"]
    solver = SOLVERS.get(task_id)
    if not solver:
        return task_id, False, f"No solver for {task_id}"

    url = f"http://localhost:{port}"

    # Reset
    resp = requests.post(f"{url}/api/reset", timeout=5)
    if resp.status_code != 200:
        return task_id, False, f"Reset failed: {resp.status_code}"

    # Re-PUT seed state (reset clears it)
    resp = requests.put(
        f"{url}/api/state",
        json=seed_state,
        headers={"Content-Type": "application/json"},
        timeout=5,
    )

    # Read current state, apply solver
    resp = requests.get(f"{url}/api/state", timeout=5)
    state = resp.json()
    try:
        solver(state)
    except Exception as e:
        return task_id, False, f"Solver error: {e}"

    # Write solved state
    resp = requests.put(
        f"{url}/api/state",
        json=state,
        headers={"Content-Type": "application/json"},
        timeout=5,
    )

    # Run verifier
    try:
        verifier = load_verifier(task["verify"])
        passed, msg = verifier(url)
        return task_id, passed, msg
    except Exception as e:
        return task_id, False, f"Verifier error: {e}"


def run_tasks_sequential(tasks, port, seed_state):
    """Run tasks sequentially on a single server."""
    proc, url = start_server(port, seed_state)
    results = []
    try:
        for task in tasks:
            result = run_single_task(task, port, seed_state)
            results.append(result)
    finally:
        stop_server(proc)
    return results


def run_tasks_parallel(tasks, workers, base_port, seed_state):
    """Run tasks in parallel across multiple servers."""
    results = []

    def worker_fn(worker_tasks, port):
        proc, url = start_server(port, seed_state)
        worker_results = []
        try:
            for task in worker_tasks:
                result = run_single_task(task, port, seed_state)
                worker_results.append(result)
        finally:
            stop_server(proc)
        return worker_results

    # Partition tasks across workers
    partitions = [[] for _ in range(workers)]
    for i, task in enumerate(tasks):
        partitions[i % workers].append(task)

    ports = [find_free_port(base_port + i * 10) for i in range(workers)]

    with ThreadPoolExecutor(max_workers=workers) as executor:
        futures = {
            executor.submit(worker_fn, partitions[i], ports[i]): i
            for i in range(workers)
            if partitions[i]
        }
        for future in as_completed(futures):
            results.extend(future.result())

    return results


# ─── Main ─────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="Real task sanity check")
    parser.add_argument("--task-id", help="Run a single task")
    parser.add_argument("--workers", type=int, default=1, help="Parallel workers")
    parser.add_argument("--port", type=int, default=9200, help="Base port")
    args = parser.parse_args()

    # Load tasks
    with open(TASKS_FILE) as f:
        all_tasks = json.load(f)

    if args.task_id:
        tasks = [t for t in all_tasks if t["id"] == args.task_id]
        if not tasks:
            print(f"Task '{args.task_id}' not found.")
            sys.exit(1)
    else:
        tasks = all_tasks

    # Generate seed state
    print("Generating seed state from data.js...")
    seed_state = generate_seed_state()
    print(f"Seed state loaded: {len(seed_state['issues'])} issues, {len(seed_state['labels'])} labels")

    # Run
    if args.workers > 1 and len(tasks) > 1:
        results = run_tasks_parallel(tasks, args.workers, args.port, seed_state)
    else:
        port = find_free_port(args.port)
        results = run_tasks_sequential(tasks, port, seed_state)

    # Sort by task id for display
    def sort_key(r):
        tid = r[0]  # e.g., "task_e1", "task_m10", "task_h20"
        prefix = tid.split("_")[1][0]  # 'e', 'm', 'h'
        num = int(tid.split("_")[1][1:])
        order = {"e": 0, "m": 1, "h": 2}
        return (order.get(prefix, 3), num)

    results.sort(key=sort_key)

    # Print results
    passed = 0
    failed = []
    for task_id, success, msg in results:
        icon = "\033[32m  PASS\033[0m" if success else "\033[31m  FAIL\033[0m"
        print(f"{icon}  {task_id:12s} {msg}")
        if success:
            passed += 1
        else:
            failed.append(task_id)

    print(f"\n{passed}/{len(results)} passed")
    if failed:
        print(f"Failed: {', '.join(failed)}")
        sys.exit(1)


if __name__ == "__main__":
    main()
