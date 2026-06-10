import requests

def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()
    issue = next((i for i in state["issues"] if i["id"] == 42), None)
    if not issue:
        return False, "Issue #42 not found."
    if issue["type"] != "issue":
        return False, f"Issue #42 type is '{issue['type']}', expected 'issue'."
    return True, "Issue #42 type changed to 'issue'."
