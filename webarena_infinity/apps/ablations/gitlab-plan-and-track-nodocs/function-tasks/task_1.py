import requests

def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."

    state = resp.json()
    match = [i for i in state["issues"] if i["title"] == "Test infrastructure setup"]
    if not match:
        return False, "Issue 'Test infrastructure setup' not found."

    issue = match[0]
    if issue["type"] != "task":
        return False, f"Issue type is '{issue['type']}', expected 'task'."

    if issue["status"] != "open":
        return False, f"Issue status is '{issue['status']}', expected 'open'."

    return True, "Issue 'Test infrastructure setup' created with type 'task'."
