import requests

def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()
    match = [i for i in state["issues"] if i["title"] == "Update SSL certificates"]
    if not match:
        return False, "Issue 'Update SSL certificates' not found."
    issue = match[0]
    if issue["dueDate"] != "2026-07-15":
        return False, f"Due date is '{issue['dueDate']}', expected '2026-07-15'."
    return True, "Issue 'Update SSL certificates' created with correct due date."
