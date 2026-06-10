import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()

    ip_label = next((l for l in state["labels"] if l["name"] == "status::in-progress"), None)
    todo_label = next((l for l in state["labels"] if l["name"] == "status::to-do"), None)
    if not ip_label or not todo_label:
        return False, "Status labels not found."
    ip_id = ip_label["id"]
    todo_id = todo_label["id"]

    # High-priority v2.1 issues should have in-progress: #19, #21, #53, #60, #63
    for issue_id in [19, 21, 53, 60, 63]:
        issue = next((i for i in state["issues"] if i["id"] == issue_id), None)
        if issue is None:
            return False, f"Issue #{issue_id} not found."
        if ip_id not in issue.get("labelIds", []):
            return False, f"Issue #{issue_id} does not have status::in-progress label."
        if todo_id in issue.get("labelIds", []):
            return False, f"Issue #{issue_id} still has status::to-do label."

    # Low-priority v2.1 issues should have to-do: #17, #50, #51, #65, #99
    for issue_id in [17, 50, 51, 65, 99]:
        issue = next((i for i in state["issues"] if i["id"] == issue_id), None)
        if issue is None:
            return False, f"Issue #{issue_id} not found."
        if todo_id not in issue.get("labelIds", []):
            return False, f"Issue #{issue_id} does not have status::to-do label."

    return True, "High-priority issues set to in-progress, low-priority to to-do."
