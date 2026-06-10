#!/usr/bin/env python3
"""Sanity check for function-task verifiers.

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
TASKS_FILE = os.path.join(APP_DIR, "function-tasks.json")
NUM_TASKS = 93


# ─── Helpers ──────────────────────────────────────────────────────────────────

def find_entity(collection, **kwargs):
    """Find a single entity by attribute match."""
    for item in collection:
        if all(item.get(k) == v for k, v in kwargs.items()):
            return item
    key_desc = ", ".join(f"{k}={v!r}" for k, v in kwargs.items())
    raise ValueError(f"Entity not found: {key_desc}")


def find_issue(state, issue_id):
    return find_entity(state["issues"], id=issue_id)


def find_label(state, name):
    return find_entity(state["labels"], name=name)


def find_milestone(state, title):
    return find_entity(state["milestones"], title=title)


def find_iteration(state, title):
    return find_entity(state["iterations"], title=title)


def find_epic(state, title):
    return find_entity(state["epics"], title=title)


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
    // Evaluate in a function scope
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


# ─── Solver Functions ─────────────────────────────────────────────────────────

def solve_task_1(state):
    """Create issue 'Test infrastructure setup' with type 'task'."""
    nid = get_next_id(state, "issues")
    state["issues"].append({
        "id": nid,
        "title": "Test infrastructure setup",
        "description": "",
        "type": "task",
        "status": "open",
        "authorId": state["currentUserId"],
        "assigneeIds": [],
        "labelIds": [],
        "milestoneId": None,
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


def solve_task_2(state):
    """Close issue #28."""
    issue = find_issue(state, 28)
    issue["status"] = "closed"
    issue["closedAt"] = "2026-03-18T00:00:00Z"


def solve_task_3(state):
    """Reopen issue #4."""
    issue = find_issue(state, 4)
    issue["status"] = "open"
    issue["closedAt"] = None


def solve_task_4(state):
    """Edit title of issue #29."""
    issue = find_issue(state, 29)
    issue["title"] = "Avatar upload fails for large PNG files"


def solve_task_5(state):
    """Assign Jun Nakamura (4) and Li Wei (7) to issue #34."""
    issue = find_issue(state, 34)
    if 4 not in issue["assigneeIds"]:
        issue["assigneeIds"].append(4)
    if 7 not in issue["assigneeIds"]:
        issue["assigneeIds"].append(7)


def solve_task_6(state):
    """Remove Jun Nakamura (4) from issue #1 assignees."""
    issue = find_issue(state, 1)
    issue["assigneeIds"] = [a for a in issue["assigneeIds"] if a != 4]


def solve_task_7(state):
    """Add 'needs-investigation' (id 19) label to issue #29."""
    issue = find_issue(state, 29)
    if 19 not in issue["labelIds"]:
        issue["labelIds"].append(19)


def solve_task_8(state):
    """Remove 'priority::high' (id 12) from issue #1."""
    issue = find_issue(state, 1)
    issue["labelIds"] = [l for l in issue["labelIds"] if l != 12]


def solve_task_9(state):
    """Set weight of issue #30 to 13."""
    issue = find_issue(state, 30)
    issue["weight"] = 13


def solve_task_10(state):
    """Set due date of issue #34 to 2026-06-01."""
    issue = find_issue(state, 34)
    issue["dueDate"] = "2026-06-01"


def solve_task_11(state):
    """Change milestone of issue #29 to v2.1 — Integrations (id 4)."""
    issue = find_issue(state, 29)
    issue["milestoneId"] = 4


def solve_task_12(state):
    """Assign issue #30 to Sprint 7 (iteration id 7)."""
    issue = find_issue(state, 30)
    issue["iterationId"] = 7


def solve_task_13(state):
    """Mark issue #46 as not confidential."""
    issue = find_issue(state, 46)
    issue["confidential"] = False


def solve_task_14(state):
    """Set time estimate on issue #31 to 4h (14400s)."""
    issue = find_issue(state, 31)
    issue["timeEstimate"] = 14400


def solve_task_15(state):
    """Add 2h time spent to issue #9 (original 7200 + 7200 = 14400)."""
    issue = find_issue(state, 9)
    issue["timeSpent"] = issue["timeSpent"] + 7200


def solve_task_16(state):
    """Create issue 'Add GraphQL support for API v3' with full fields."""
    nid = get_next_id(state, "issues")
    state["issues"].append({
        "id": nid,
        "title": "Add GraphQL support for API v3",
        "description": "",
        "type": "issue",
        "status": "open",
        "authorId": state["currentUserId"],
        "assigneeIds": [6],  # Tom Ramirez
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


def solve_task_17(state):
    """Create confidential issue 'Security audit findings Q1' with security label."""
    nid = get_next_id(state, "issues")
    state["issues"].append({
        "id": nid,
        "title": "Security audit findings Q1",
        "description": "",
        "type": "issue",
        "status": "open",
        "authorId": state["currentUserId"],
        "assigneeIds": [],
        "labelIds": [5],  # security
        "milestoneId": None,
        "iterationId": None,
        "weight": None,
        "dueDate": None,
        "confidential": True,
        "timeEstimate": 0,
        "timeSpent": 0,
        "createdAt": "2026-03-18T00:00:00Z",
        "updatedAt": "2026-03-18T00:00:00Z",
        "closedAt": None,
        "relatedIssues": [],
    })


def solve_task_18(state):
    """Add comment 'This is ready for review.' on issue #14."""
    nid = get_next_id(state, "comments")
    state["comments"].append({
        "id": nid,
        "issueId": 14,
        "authorId": state["currentUserId"],
        "body": "This is ready for review.",
        "createdAt": "2026-03-18T00:00:00Z",
        "updatedAt": "2026-03-18T00:00:00Z",
        "type": "comment",
    })


def solve_task_19(state):
    """Close issue #31."""
    issue = find_issue(state, 31)
    issue["status"] = "closed"
    issue["closedAt"] = "2026-03-18T00:00:00Z"


def solve_task_20(state):
    """Assign Emily Okonkwo (id 8) to issue #34 via quick action."""
    issue = find_issue(state, 34)
    if 8 not in issue["assigneeIds"]:
        issue["assigneeIds"].append(8)


def solve_task_21(state):
    """Add 'breaking-change' (id 20) label to issue #9."""
    issue = find_issue(state, 9)
    if 20 not in issue["labelIds"]:
        issue["labelIds"].append(20)


def solve_task_22(state):
    """Replace priority::high (12) with priority::critical (11) on issue #35."""
    issue = find_issue(state, 35)
    issue["labelIds"] = [l for l in issue["labelIds"] if l != 12]
    if 11 not in issue["labelIds"]:
        issue["labelIds"].append(11)


def solve_task_23(state):
    """Change issue #28 milestone to Backlog (id 6)."""
    issue = find_issue(state, 28)
    issue["milestoneId"] = 6


def solve_task_24(state):
    """Set weight of issue #72 to 5."""
    issue = find_issue(state, 72)
    issue["weight"] = 5


def solve_task_25(state):
    """Set due date of issue #37 to 2026-05-01."""
    issue = find_issue(state, 37)
    issue["dueDate"] = "2026-05-01"


def solve_task_26(state):
    """Set time estimate of issue #32 to 8h (28800s)."""
    issue = find_issue(state, 32)
    issue["timeEstimate"] = 28800


def solve_task_27(state):
    """Add 3h30m (12600s) time spent to issue #3."""
    issue = find_issue(state, 3)
    issue["timeSpent"] = issue["timeSpent"] + 12600


def solve_task_28(state):
    """Create label 'infrastructure' with color '#2ecc71'."""
    nid = get_next_id(state, "labels")
    state["labels"].append({
        "id": nid,
        "name": "infrastructure",
        "description": "",
        "color": "#2ecc71",
        "textColor": "#fff",
        "scoped": False,
    })


def solve_task_29(state):
    """Create scoped label 'env::production' with color '#e74c3c'."""
    nid = get_next_id(state, "labels")
    state["labels"].append({
        "id": nid,
        "name": "env::production",
        "description": "",
        "color": "#e74c3c",
        "textColor": "#fff",
        "scoped": True,
    })


def solve_task_30(state):
    """Change description of 'tech-debt' label."""
    label = find_label(state, "tech-debt")
    label["description"] = "Legacy code cleanup and refactoring"


def solve_task_31(state):
    """Change color of 'bug' label to '#ff0000'."""
    label = find_label(state, "bug")
    label["color"] = "#ff0000"


def solve_task_32(state):
    """Delete 'needs-investigation' label (id 19) and clean up references."""
    label = find_label(state, "needs-investigation")
    label_id = label["id"]
    state["labels"] = [l for l in state["labels"] if l["id"] != label_id]
    for issue in state["issues"]:
        issue["labelIds"] = [l for l in issue["labelIds"] if l != label_id]
    for epic in state["epics"]:
        epic["labels"] = [l for l in epic["labels"] if l != label_id]
    for board in state["boards"]:
        board["lists"] = [l for l in board["lists"] if l.get("labelId") != label_id]


def solve_task_33(state):
    """Create milestone 'v3.1 — Analytics'."""
    nid = get_next_id(state, "milestones")
    state["milestones"].append({
        "id": nid,
        "title": "v3.1 \u2014 Analytics",
        "description": "",
        "startDate": "2026-11-01",
        "dueDate": "2027-01-31",
        "status": "active",
    })


def solve_task_34(state):
    """Change Backlog milestone description."""
    ms = find_milestone(state, "Backlog")
    ms["description"] = "Unscheduled items awaiting prioritization"


def solve_task_35(state):
    """Close milestone 'v2.0 — API Overhaul'."""
    ms = find_milestone(state, "v2.0 \u2014 API Overhaul")
    ms["status"] = "closed"


def solve_task_36(state):
    """Reopen milestone 'v1.0 — Foundation'."""
    ms = find_milestone(state, "v1.0 \u2014 Foundation")
    ms["status"] = "active"


def solve_task_37(state):
    """Delete milestone 'v1.2 — Hotfixes' (id 7) and clean up references."""
    ms = find_milestone(state, "v1.2 \u2014 Hotfixes")
    ms_id = ms["id"]
    state["milestones"] = [m for m in state["milestones"] if m["id"] != ms_id]
    for issue in state["issues"]:
        if issue["milestoneId"] == ms_id:
            issue["milestoneId"] = None


def solve_task_38(state):
    """Create iteration 'Sprint 9' in Engineering Sprints cadence."""
    nid = get_next_id(state, "iterations")
    state["iterations"].append({
        "id": nid,
        "cadenceId": 1,  # Engineering Sprints
        "title": "Sprint 9",
        "startDate": "2026-04-28",
        "endDate": "2026-05-11",
        "status": "upcoming",
    })


def solve_task_39(state):
    """Delete iteration 'Sprint 8' and clean up references."""
    iteration = find_iteration(state, "Sprint 8")
    iter_id = iteration["id"]
    state["iterations"] = [i for i in state["iterations"] if i["id"] != iter_id]
    for issue in state["issues"]:
        if issue["iterationId"] == iter_id:
            issue["iterationId"] = None


def solve_task_40(state):
    """Create epic 'Internationalization (i18n)'."""
    nid = get_next_id(state, "epics")
    state["epics"].append({
        "id": nid,
        "title": "Internationalization (i18n)",
        "description": "Add multi-language support across the platform",
        "status": "open",
        "startDate": None,
        "dueDate": None,
        "labels": [],
        "authorId": state["currentUserId"],
        "confidential": False,
        "childIssueIds": [],
        "childEpicIds": [],
        "createdAt": "2026-03-18T00:00:00Z",
        "updatedAt": "2026-03-18T00:00:00Z",
    })


def solve_task_41(state):
    """Close epic 'Performance Optimization Phase 2'."""
    epic = find_epic(state, "Performance Optimization Phase 2")
    epic["status"] = "closed"


def solve_task_42(state):
    """Reopen epic 'Data Export & Reporting'."""
    epic = find_epic(state, "Data Export & Reporting")
    epic["status"] = "open"


def solve_task_43(state):
    """Add issue #30 to epic 'Mobile Responsive Redesign'."""
    epic = find_epic(state, "Mobile Responsive Redesign")
    if 30 not in epic["childIssueIds"]:
        epic["childIssueIds"].append(30)


def solve_task_44(state):
    """Remove issue #45 from epic 'User Authentication Overhaul'."""
    epic = find_epic(state, "User Authentication Overhaul")
    epic["childIssueIds"] = [i for i in epic["childIssueIds"] if i != 45]


def solve_task_45(state):
    """Add board list for 'bug' label (id 1) to Development Board."""
    board = find_board(state, "Development Board")
    nid = get_next_id(state, "boardLists")
    # Insert before closed list
    closed_idx = next((i for i, l in enumerate(board["lists"]) if l["type"] == "closed"), len(board["lists"]))
    board["lists"].insert(closed_idx, {
        "id": nid,
        "type": "label",
        "title": "bug",
        "position": closed_idx,
        "labelId": 1,
    })
    # Re-index positions
    for i, lst in enumerate(board["lists"]):
        lst["position"] = i


def solve_task_46(state):
    """Remove 'Done' list (labelId 18) from Development Board."""
    board = find_board(state, "Development Board")
    board["lists"] = [l for l in board["lists"] if l.get("labelId") != 18]
    for i, lst in enumerate(board["lists"]):
        lst["position"] = i


def solve_task_47(state):
    """Add blocks relationship from issue #12 to #49."""
    issue12 = find_issue(state, 12)
    issue49 = find_issue(state, 49)
    if not any(r["issueId"] == 49 for r in issue12["relatedIssues"]):
        issue12["relatedIssues"].append({"issueId": 49, "type": "blocks"})
    if not any(r["issueId"] == 12 for r in issue49["relatedIssues"]):
        issue49["relatedIssues"].append({"issueId": 12, "type": "is_blocked_by"})


def solve_task_48(state):
    """Add related_to relationship between issue #28 and #31."""
    issue28 = find_issue(state, 28)
    issue31 = find_issue(state, 31)
    if not any(r["issueId"] == 31 for r in issue28["relatedIssues"]):
        issue28["relatedIssues"].append({"issueId": 31, "type": "related_to"})
    if not any(r["issueId"] == 28 for r in issue31["relatedIssues"]):
        issue31["relatedIssues"].append({"issueId": 28, "type": "related_to"})


def solve_task_49(state):
    """Remove related issue link between #1 and #2."""
    issue1 = find_issue(state, 1)
    issue2 = find_issue(state, 2)
    issue1["relatedIssues"] = [r for r in issue1["relatedIssues"] if r["issueId"] != 2]
    issue2["relatedIssues"] = [r for r in issue2["relatedIssues"] if r["issueId"] != 1]


def solve_task_50(state):
    """Bulk close issues #67, #72, #120."""
    for issue_id in [67, 72, 120]:
        issue = find_issue(state, issue_id)
        issue["status"] = "closed"
        issue["closedAt"] = "2026-03-18T00:00:00Z"


def solve_task_51(state):
    """Bulk assign issues #34, #68, #70 to Priya Sharma (id 5)."""
    for issue_id in [34, 68, 70]:
        issue = find_issue(state, issue_id)
        if 5 not in issue["assigneeIds"]:
            issue["assigneeIds"].append(5)


def solve_task_52(state):
    """Bulk add 'tech-debt' (id 10) label to issues #29 and #37."""
    for issue_id in [29, 37]:
        issue = find_issue(state, issue_id)
        if 10 not in issue["labelIds"]:
            issue["labelIds"].append(10)


def solve_task_53(state):
    """Bulk set milestone to Backlog (id 6) for issues #66, #96, #98."""
    for issue_id in [66, 96, 98]:
        issue = find_issue(state, issue_id)
        issue["milestoneId"] = 6


def solve_task_54(state):
    """Mark notification #1 as read."""
    notif = find_entity(state["notifications"], id=1)
    notif["read"] = True


def solve_task_55(state):
    """Mark all notifications as read."""
    for n in state["notifications"]:
        n["read"] = True


def solve_task_56(state):
    """Change notification settings level to 'on_mention'."""
    state["notificationSettings"]["level"] = "on_mention"


def solve_task_57(state):
    """Subscribe to issue #33."""
    if "subscriptions" not in state:
        state["subscriptions"] = []
    if 33 not in state["subscriptions"]:
        state["subscriptions"].append(33)


def solve_task_58(state):
    """Create issue 'Production database outage alert' with type 'incident'."""
    nid = get_next_id(state, "issues")
    state["issues"].append({
        "id": nid,
        "title": "Production database outage alert",
        "description": "",
        "type": "incident",
        "status": "open",
        "authorId": state["currentUserId"],
        "assigneeIds": [],
        "labelIds": [],
        "milestoneId": None,
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


def solve_task_59(state):
    """Edit description of issue #30."""
    issue = find_issue(state, 30)
    issue["description"] = "Implement dark mode with system preference detection and manual toggle."


def solve_task_60(state):
    """Mark issue #34 as confidential."""
    issue = find_issue(state, 34)
    issue["confidential"] = True


def solve_task_61(state):
    """Clear weight of issue #28."""
    issue = find_issue(state, 28)
    issue["weight"] = None


def solve_task_62(state):
    """Clear due date of issue #28."""
    issue = find_issue(state, 28)
    issue["dueDate"] = None


def solve_task_63(state):
    """Remove milestone from issue #29."""
    issue = find_issue(state, 29)
    issue["milestoneId"] = None


def solve_task_64(state):
    """Remove iteration from issue #1."""
    issue = find_issue(state, 1)
    issue["iterationId"] = None


def solve_task_65(state):
    """Close issue #9 via /close quick action."""
    issue = find_issue(state, 9)
    issue["status"] = "closed"
    issue["closedAt"] = "2026-03-18T00:00:00Z"


def solve_task_66(state):
    """Reopen issue #4 via /reopen quick action."""
    issue = find_issue(state, 4)
    issue["status"] = "open"
    issue["closedAt"] = None


def solve_task_67(state):
    """Remove Li Wei (id 7) from issue #3 via /unassign."""
    issue = find_issue(state, 3)
    issue["assigneeIds"] = [a for a in issue["assigneeIds"] if a != 7]


def solve_task_68(state):
    """Remove 'performance' label (id 4) from issue #9 via /unlabel."""
    issue = find_issue(state, 9)
    issue["labelIds"] = [l for l in issue["labelIds"] if l != 4]


def solve_task_69(state):
    """Create issue 'Add user activity dashboard' with description."""
    nid = get_next_id(state, "issues")
    state["issues"].append({
        "id": nid,
        "title": "Add user activity dashboard",
        "description": "Build a dashboard showing user login history, recent actions, and usage statistics.",
        "type": "issue",
        "status": "open",
        "authorId": state["currentUserId"],
        "assigneeIds": [],
        "labelIds": [],
        "milestoneId": None,
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


def solve_task_70(state):
    """Create issue 'Update SSL certificates' with due date."""
    nid = get_next_id(state, "issues")
    state["issues"].append({
        "id": nid,
        "title": "Update SSL certificates",
        "description": "",
        "type": "issue",
        "status": "open",
        "authorId": state["currentUserId"],
        "assigneeIds": [],
        "labelIds": [],
        "milestoneId": None,
        "iterationId": None,
        "weight": None,
        "dueDate": "2026-07-15",
        "confidential": False,
        "timeEstimate": 0,
        "timeSpent": 0,
        "createdAt": "2026-03-18T00:00:00Z",
        "updatedAt": "2026-03-18T00:00:00Z",
        "closedAt": None,
        "relatedIssues": [],
    })


def solve_task_71(state):
    """Create issue 'Sprint 7 planning notes' with iteration Sprint 7 (id 7)."""
    nid = get_next_id(state, "issues")
    state["issues"].append({
        "id": nid,
        "title": "Sprint 7 planning notes",
        "description": "",
        "type": "issue",
        "status": "open",
        "authorId": state["currentUserId"],
        "assigneeIds": [],
        "labelIds": [],
        "milestoneId": None,
        "iterationId": 7,
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


def solve_task_72(state):
    """Rename 'tech-debt' label (id 10) to 'technical-debt'."""
    label = find_label(state, "tech-debt")
    label["name"] = "technical-debt"


def solve_task_73(state):
    """Create label 'blocked' with color and description."""
    nid = get_next_id(state, "labels")
    state["labels"].append({
        "id": nid,
        "name": "blocked",
        "description": "Work is blocked by external dependencies",
        "color": "#e74c3c",
        "textColor": "#fff",
        "scoped": False,
    })


def solve_task_74(state):
    """Rename 'Backlog' milestone (id 6) to 'Product Backlog'."""
    ms = find_milestone(state, "Backlog")
    ms["title"] = "Product Backlog"


def solve_task_75(state):
    """Update v2.1 — Integrations milestone dates."""
    ms = find_milestone(state, "v2.1 \u2014 Integrations")
    ms["startDate"] = "2026-05-15"
    ms["dueDate"] = "2026-07-15"


def solve_task_76(state):
    """Create iteration 'Design Cycle 6' in Design Cycles cadence."""
    nid = get_next_id(state, "iterations")
    state["iterations"].append({
        "id": nid,
        "cadenceId": 2,  # Design Cycles
        "title": "Design Cycle 6",
        "startDate": "2026-04-21",
        "endDate": "2026-05-11",
        "status": "upcoming",
    })


def solve_task_77(state):
    """Create epic 'Documentation Overhaul' with dates."""
    nid = get_next_id(state, "epics")
    state["epics"].append({
        "id": nid,
        "title": "Documentation Overhaul",
        "description": "",
        "status": "open",
        "startDate": "2026-06-01",
        "dueDate": "2026-08-31",
        "labels": [],
        "authorId": state["currentUserId"],
        "confidential": False,
        "childIssueIds": [],
        "childEpicIds": [],
        "createdAt": "2026-03-18T00:00:00Z",
        "updatedAt": "2026-03-18T00:00:00Z",
    })


def solve_task_78(state):
    """Create confidential epic 'Security Penetration Testing'."""
    nid = get_next_id(state, "epics")
    state["epics"].append({
        "id": nid,
        "title": "Security Penetration Testing",
        "description": "",
        "status": "open",
        "startDate": None,
        "dueDate": None,
        "labels": [],
        "authorId": state["currentUserId"],
        "confidential": True,
        "childIssueIds": [],
        "childEpicIds": [],
        "createdAt": "2026-03-18T00:00:00Z",
        "updatedAt": "2026-03-18T00:00:00Z",
    })


def solve_task_79(state):
    """Add is_blocked_by from #16 to #15, blocks from #15 to #16."""
    issue16 = find_issue(state, 16)
    issue15 = find_issue(state, 15)
    if not any(r["issueId"] == 15 for r in issue16["relatedIssues"]):
        issue16["relatedIssues"].append({"issueId": 15, "type": "is_blocked_by"})
    if not any(r["issueId"] == 16 for r in issue15["relatedIssues"]):
        issue15["relatedIssues"].append({"issueId": 16, "type": "blocks"})


def solve_task_80(state):
    """Delete 'documentation' label (id 3) and clean up references."""
    label = find_label(state, "documentation")
    label_id = label["id"]
    state["labels"] = [l for l in state["labels"] if l["id"] != label_id]
    for issue in state["issues"]:
        issue["labelIds"] = [l for l in issue["labelIds"] if l != label_id]
    for epic in state["epics"]:
        epic["labels"] = [l for l in epic["labels"] if l != label_id]
    for board in state["boards"]:
        board["lists"] = [l for l in board["lists"] if l.get("labelId") != label_id]


def solve_task_81(state):
    """Delete 'Backlog' milestone (id 6) and clean up references."""
    ms = find_milestone(state, "Backlog")
    ms_id = ms["id"]
    state["milestones"] = [m for m in state["milestones"] if m["id"] != ms_id]
    for issue in state["issues"]:
        if issue["milestoneId"] == ms_id:
            issue["milestoneId"] = None


def solve_task_82(state):
    """Create issue 'Investigate flaky test suite' with labels bug (1) and backend (7)."""
    nid = get_next_id(state, "issues")
    state["issues"].append({
        "id": nid,
        "title": "Investigate flaky test suite",
        "description": "",
        "type": "issue",
        "status": "open",
        "authorId": state["currentUserId"],
        "assigneeIds": [],
        "labelIds": [1, 7],
        "milestoneId": None,
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


def solve_task_83(state):
    """Assign Ana Garcia (id 3) to issue #57."""
    issue = find_issue(state, 57)
    if 3 not in issue["assigneeIds"]:
        issue["assigneeIds"].append(3)


def solve_task_84(state):
    """Add labels 'devops' (9) and 'tech-debt' (10) to issue #52."""
    issue = find_issue(state, 52)
    if 9 not in issue["labelIds"]:
        issue["labelIds"].append(9)
    if 10 not in issue["labelIds"]:
        issue["labelIds"].append(10)


def solve_task_85(state):
    """Disable email notifications."""
    state["notificationSettings"]["email"] = False


def solve_task_86(state):
    """Change notification level to 'disabled'."""
    state["notificationSettings"]["level"] = "disabled"


def solve_task_87(state):
    """Add board list for 'feature' label (id 2) to Development Board."""
    board = find_board(state, "Development Board")
    nid = get_next_id(state, "boardLists")
    closed_idx = next((i for i, l in enumerate(board["lists"]) if l["type"] == "closed"), len(board["lists"]))
    board["lists"].insert(closed_idx, {
        "id": nid,
        "type": "label",
        "title": "feature",
        "position": closed_idx,
        "labelId": 2,
    })
    for i, lst in enumerate(board["lists"]):
        lst["position"] = i


def solve_task_88(state):
    """Change issue #42 type from 'task' to 'issue'."""
    issue = find_issue(state, 42)
    issue["type"] = "issue"


def solve_task_89(state):
    """Change issue #11 priority from critical (11) to medium (13)."""
    issue = find_issue(state, 11)
    issue["labelIds"] = [l for l in issue["labelIds"] if l != 11]
    if 13 not in issue["labelIds"]:
        issue["labelIds"].append(13)


def solve_task_90(state):
    """Add issue #66 to epic 'Notification System Revamp'."""
    epic = find_epic(state, "Notification System Revamp")
    if 66 not in epic["childIssueIds"]:
        epic["childIssueIds"].append(66)


def solve_task_91(state):
    """Delete iteration 'Sprint 3' and clean up references."""
    iteration = find_iteration(state, "Sprint 3")
    iter_id = iteration["id"]
    state["iterations"] = [i for i in state["iterations"] if i["id"] != iter_id]
    for issue in state["issues"]:
        if issue["iterationId"] == iter_id:
            issue["iterationId"] = None


def solve_task_92(state):
    """Bulk close issues #33, #42, #50."""
    for issue_id in [33, 42, 50]:
        issue = find_issue(state, issue_id)
        issue["status"] = "closed"
        issue["closedAt"] = "2026-03-18T00:00:00Z"


def solve_task_93(state):
    """Bulk assign issues #52, #57, #58 to David Kim (id 11)."""
    for issue_id in [52, 57, 58]:
        issue = find_issue(state, issue_id)
        if 11 not in issue["assigneeIds"]:
            issue["assigneeIds"].append(11)


# ─── Solver Registry ──────────────────────────────────────────────────────────

SOLVERS = {
    f"task_{i}": globals()[f"solve_task_{i}"]
    for i in range(1, NUM_TASKS + 1)
}


# ─── Server Management ───────────────────────────────────────────────────────

def find_free_port(start=9100):
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
    parser = argparse.ArgumentParser(description="Function task sanity check")
    parser.add_argument("--task-id", help="Run a single task")
    parser.add_argument("--workers", type=int, default=1, help="Parallel workers")
    parser.add_argument("--port", type=int, default=9100, help="Base port")
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

    # Sort by task id
    results.sort(key=lambda r: int(r[0].split("_")[1]))

    # Print results
    passed = 0
    failed = []
    for task_id, success, msg in results:
        status = "PASS" if success else "FAIL"
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
