import requests

def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()
    issue = next((i for i in state["issues"] if i["id"] == 57), None)
    if not issue:
        return False, "Issue #57 not found."
    if 3 not in issue["assigneeIds"]:
        return False, "Ana Garcia (id 3) is not assigned to issue #57."
    return True, "Ana Garcia assigned to issue #57."
