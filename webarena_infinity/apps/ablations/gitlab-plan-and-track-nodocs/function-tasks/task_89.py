import requests

def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()
    issue = next((i for i in state["issues"] if i["id"] == 11), None)
    if not issue:
        return False, "Issue #11 not found."
    if 11 in issue["labelIds"]:
        return False, "Label 'priority::critical' (id 11) still present on issue #11."
    if 13 not in issue["labelIds"]:
        return False, "Label 'priority::medium' (id 13) not found on issue #11."
    return True, "Issue #11 priority changed from critical to medium."
