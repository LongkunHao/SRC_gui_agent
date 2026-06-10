import requests

def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()

    issue = next((i for i in state["issues"] if i["id"] == 14), None)
    if issue is None:
        return False, "Issue #14 not found."

    if 11 not in issue["labelIds"]:
        return False, "Issue #14 does not have the priority::critical label (id 11)."

    if 12 in issue["labelIds"]:
        return False, "Issue #14 still has the priority::high label (id 12)."

    return True, "Issue #14 has critical priority and no longer has high priority."
