import requests

def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()

    issue = next((i for i in state["issues"] if i["id"] == 20), None)
    if issue is None:
        return False, "Issue #20 not found."

    if issue["dueDate"] != "2026-05-15":
        return False, f"Issue #20 due date is '{issue['dueDate']}', expected '2026-05-15'."

    return True, "Issue #20 due date is set to '2026-05-15'."
