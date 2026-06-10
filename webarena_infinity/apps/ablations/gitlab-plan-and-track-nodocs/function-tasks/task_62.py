import requests

def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()
    issue = next((i for i in state["issues"] if i["id"] == 28), None)
    if not issue:
        return False, "Issue #28 not found."
    if issue["dueDate"] is not None:
        return False, f"Issue #28 due date is '{issue['dueDate']}', expected None."
    return True, "Issue #28 due date cleared successfully."
