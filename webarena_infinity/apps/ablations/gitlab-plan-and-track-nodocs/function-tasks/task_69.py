import requests

def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()
    match = [i for i in state["issues"] if i["title"] == "Add user activity dashboard"]
    if not match:
        return False, "Issue 'Add user activity dashboard' not found."
    issue = match[0]
    expected_desc = "Build a dashboard showing user login history, recent actions, and usage statistics."
    if issue["description"] != expected_desc:
        return False, f"Description doesn't match. Got: '{issue['description'][:80]}...'"
    return True, "Issue 'Add user activity dashboard' created with correct description."
