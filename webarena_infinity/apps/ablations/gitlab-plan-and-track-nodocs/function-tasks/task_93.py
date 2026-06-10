import requests

def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()
    for issue_id in [52, 57, 58]:
        issue = next((i for i in state["issues"] if i["id"] == issue_id), None)
        if not issue:
            return False, f"Issue #{issue_id} not found."
        if 11 not in issue["assigneeIds"]:
            return False, f"David Kim (id 11) not assigned to issue #{issue_id}."
    return True, "Issues #52, #57, and #58 bulk assigned to David Kim."
