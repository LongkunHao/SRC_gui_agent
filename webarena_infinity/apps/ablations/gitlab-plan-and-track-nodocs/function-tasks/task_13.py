import requests

def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."

    state = resp.json()
    issue = next((i for i in state["issues"] if i["id"] == 46), None)
    if not issue:
        return False, "Issue #46 not found."

    if issue["confidential"] is not False:
        return False, f"Issue #46 confidential is {issue['confidential']}, expected False."

    return True, "Issue #46 marked as not confidential."
