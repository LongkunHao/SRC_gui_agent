import requests

def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()

    for issue_id in [57, 58, 59]:
        issue = next((i for i in state["issues"] if i["id"] == issue_id), None)
        if issue is None:
            return False, f"Issue #{issue_id} not found."
        if 2 not in issue.get("assigneeIds", []):
            return False, f"Marek Kowalski (id 2) not in assigneeIds for issue #{issue_id}: {issue.get('assigneeIds')}."

    return True, "Marek Kowalski assigned to unassigned security v3.0 issues (#57, #58, #59)."
