import requests

def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()
    issue = next((i for i in state["issues"] if i["id"] == 9), None)
    if not issue:
        return False, "Issue #9 not found."
    if issue["status"] != "closed":
        return False, f"Issue #9 status is '{issue['status']}', expected 'closed'."
    return True, "Issue #9 closed via /close quick action."
