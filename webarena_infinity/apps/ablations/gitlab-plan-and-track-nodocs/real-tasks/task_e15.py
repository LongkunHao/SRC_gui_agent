import requests

def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()

    issue = next((i for i in state["issues"] if i["id"] == 104), None)
    if issue is None:
        return False, "Issue #104 not found."

    if 1 in issue["labelIds"]:
        return False, "Issue #104 still has the bug label (id 1)."

    return True, "Issue #104 no longer has the bug label (id 1)."
