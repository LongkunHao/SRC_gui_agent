import requests

def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()
    issue = next((i for i in state["issues"] if i["id"] == 1), None)
    if not issue:
        return False, "Issue #1 not found."
    if issue["iterationId"] is not None:
        return False, f"Issue #1 iterationId is {issue['iterationId']}, expected None."
    return True, "Issue #1 iteration removed successfully."
