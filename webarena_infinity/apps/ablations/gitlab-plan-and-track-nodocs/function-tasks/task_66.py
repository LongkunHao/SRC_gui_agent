import requests

def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()
    issue = next((i for i in state["issues"] if i["id"] == 4), None)
    if not issue:
        return False, "Issue #4 not found."
    if issue["status"] != "open":
        return False, f"Issue #4 status is '{issue['status']}', expected 'open'."
    if issue["closedAt"] is not None:
        return False, f"Issue #4 closedAt should be null after reopening."
    return True, "Issue #4 reopened via /reopen quick action."
