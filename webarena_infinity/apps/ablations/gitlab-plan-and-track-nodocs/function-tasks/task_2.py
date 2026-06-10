import requests

def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."

    state = resp.json()
    issue = next((i for i in state["issues"] if i["id"] == 28), None)
    if not issue:
        return False, "Issue #28 not found."

    if issue["status"] != "closed":
        return False, f"Issue #28 status is '{issue['status']}', expected 'closed'."

    return True, "Issue #28 closed successfully."
