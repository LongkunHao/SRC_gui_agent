import requests

def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()

    issue = next((i for i in state["issues"] if i["id"] == 57), None)
    if issue is None:
        return False, "Issue #57 not found."

    if issue["confidential"] is not False:
        return False, f"Issue #57 confidential is {issue['confidential']}, expected False."

    return True, "Issue #57 is no longer confidential."
