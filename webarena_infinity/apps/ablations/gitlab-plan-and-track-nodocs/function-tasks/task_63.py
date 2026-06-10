import requests

def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()
    issue = next((i for i in state["issues"] if i["id"] == 29), None)
    if not issue:
        return False, "Issue #29 not found."
    if issue["milestoneId"] is not None:
        return False, f"Issue #29 milestoneId is {issue['milestoneId']}, expected None."
    return True, "Issue #29 milestone removed successfully."
