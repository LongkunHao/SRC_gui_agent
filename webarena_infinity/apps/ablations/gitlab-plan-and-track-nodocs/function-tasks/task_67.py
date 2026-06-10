import requests

def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()
    issue = next((i for i in state["issues"] if i["id"] == 3), None)
    if not issue:
        return False, "Issue #3 not found."
    if 7 in issue["assigneeIds"]:
        return False, "Li Wei (id 7) is still assigned to issue #3."
    return True, "Li Wei removed from issue #3 via /unassign quick action."
