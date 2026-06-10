import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()

    # Epic 2 (API v3 Migration) has highest total open-child weight (47).
    # Its to-do children (label 15): #8, #47 — should now have in-progress (label 16).
    todo_id = next(l["id"] for l in state["labels"] if l["name"] == "status::to-do")
    ip_id = next(l["id"] for l in state["labels"] if l["name"] == "status::in-progress")

    for issue_id in [8, 47]:
        issue = next((i for i in state["issues"] if i["id"] == issue_id), None)
        if issue is None:
            return False, f"Issue #{issue_id} not found."
        if ip_id not in issue.get("labelIds", []):
            return False, (
                f"Issue #{issue_id} does not have status::in-progress. "
                f"Labels: {issue.get('labelIds')}."
            )
        if todo_id in issue.get("labelIds", []):
            return False, (
                f"Issue #{issue_id} still has status::to-do."
            )

    return True, "API v3 Migration epic's to-do children changed to in-progress."
