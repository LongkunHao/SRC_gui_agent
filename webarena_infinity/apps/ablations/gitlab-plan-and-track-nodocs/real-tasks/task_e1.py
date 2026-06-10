import requests

def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()

    issue = next((i for i in state["issues"] if i["id"] == 33), None)
    if issue is None:
        return False, "Issue #33 not found."

    if issue["status"] != "closed":
        return False, f"Issue #33 status is '{issue['status']}', expected 'closed'."

    return True, "Issue #33 'Memory leak in WebSocket connection handler' is closed."
