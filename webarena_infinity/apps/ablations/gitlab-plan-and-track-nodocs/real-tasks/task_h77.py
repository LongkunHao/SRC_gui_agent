import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()

    # Epic 1 (User Authentication Overhaul) has highest total time spent (61200s).
    # Original dueDate: 2026-04-30 → extended by 30 days → 2026-05-30
    epic1 = next((e for e in state["epics"] if e["id"] == 1), None)
    if epic1 is None:
        return False, "Epic 'User Authentication Overhaul' (id 1) not found."
    if epic1.get("dueDate") != "2026-05-30":
        return False, (
            f"Epic 1 dueDate is '{epic1.get('dueDate')}', expected '2026-05-30'."
        )

    # Open children with no time spent: #2, #45, #46 — should have priority::high
    high_id = next(l["id"] for l in state["labels"] if l["name"] == "priority::high")
    priority_ids = {l["id"] for l in state["labels"] if l["name"].startswith("priority::")}

    for issue_id in [2, 45, 46]:
        issue = next((i for i in state["issues"] if i["id"] == issue_id), None)
        if issue is None:
            return False, f"Issue #{issue_id} not found."
        if high_id not in issue.get("labelIds", []):
            return False, (
                f"Issue #{issue_id} does not have priority::high. "
                f"Labels: {issue.get('labelIds')}."
            )
        other_priority = [l for l in issue.get("labelIds", [])
                          if l in priority_ids and l != high_id]
        if other_priority:
            return False, (
                f"Issue #{issue_id} has extra priority labels: {other_priority}."
            )

    return True, "Auth Overhaul epic due extended, unlogged children set to high priority."
