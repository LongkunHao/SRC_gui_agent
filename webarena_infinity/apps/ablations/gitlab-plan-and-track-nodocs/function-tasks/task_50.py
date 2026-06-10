import requests

def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."

    state = resp.json()
    for issue_id in [67, 72, 120]:
        issue = next((i for i in state["issues"] if i["id"] == issue_id), None)
        if not issue:
            return False, f"Issue #{issue_id} not found."
        if issue["status"] != "closed":
            return False, f"Issue #{issue_id} status is '{issue['status']}', expected 'closed'."

    return True, "Issues #67, #72, and #120 bulk closed."
