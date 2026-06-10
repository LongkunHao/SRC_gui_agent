import requests

def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()
    issue = next((i for i in state["issues"] if i["id"] == 34), None)
    if not issue:
        return False, "Issue #34 not found."
    if issue["confidential"] is not True:
        return False, f"Issue #34 confidential is {issue['confidential']}, expected True."
    return True, "Issue #34 marked as confidential."
