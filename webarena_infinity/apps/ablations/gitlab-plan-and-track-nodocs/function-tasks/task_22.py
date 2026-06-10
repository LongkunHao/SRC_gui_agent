import requests

def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."

    state = resp.json()
    issue = next((i for i in state["issues"] if i["id"] == 35), None)
    if not issue:
        return False, "Issue #35 not found."

    # priority::critical = id 11, priority::high = id 12
    if 11 not in issue["labelIds"]:
        return False, "Label 'priority::critical' (id 11) not found on issue #35."

    if 12 in issue["labelIds"]:
        return False, "Label 'priority::high' (id 12) should have been replaced by 'priority::critical'."

    return True, "Issue #35 priority changed from high to critical via scoped label replacement."
