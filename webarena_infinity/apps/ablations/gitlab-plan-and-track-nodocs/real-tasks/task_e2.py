import requests

def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()

    issue = next((i for i in state["issues"] if i["id"] == 89), None)
    if issue is None:
        return False, "Issue #89 not found."

    if issue["status"] != "open":
        return False, f"Issue #89 status is '{issue['status']}', expected 'open'."

    return True, "Issue #89 'Fix data loss on concurrent issue edits' is reopened."
