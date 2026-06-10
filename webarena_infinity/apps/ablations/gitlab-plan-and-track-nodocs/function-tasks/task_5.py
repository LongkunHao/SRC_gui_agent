import requests

def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."

    state = resp.json()
    issue = next((i for i in state["issues"] if i["id"] == 34), None)
    if not issue:
        return False, "Issue #34 not found."

    # Jun Nakamura = id 4, Li Wei = id 7
    if 4 not in issue["assigneeIds"]:
        return False, "Jun Nakamura (id 4) is not assigned to issue #34."

    if 7 not in issue["assigneeIds"]:
        return False, "Li Wei (id 7) is not assigned to issue #34."

    return True, "Issue #34 assigned to Jun Nakamura and Li Wei."
