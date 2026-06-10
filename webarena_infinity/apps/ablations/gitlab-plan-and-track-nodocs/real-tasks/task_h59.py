import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()

    epic = next(
        (e for e in state["epics"] if "User Authentication Overhaul" in e.get("title", "")),
        None,
    )
    if epic is None:
        return False, "Epic 'User Authentication Overhaul' not found."

    if epic.get("startDate") != "2026-03-01":
        return False, f"Epic startDate is '{epic.get('startDate')}', expected '2026-03-01'."

    # Open children: #1, #2, #3, #45, #46 — all should be confidential
    for issue_id in [1, 2, 3, 45, 46]:
        issue = next((i for i in state["issues"] if i["id"] == issue_id), None)
        if issue is None:
            return False, f"Issue #{issue_id} not found."
        if issue["status"] != "open":
            continue  # only check open ones
        if not issue.get("confidential"):
            return False, f"Issue #{issue_id} confidential is {issue.get('confidential')}, expected True."

    return True, "Auth Overhaul epic startDate updated, all open children are confidential."
