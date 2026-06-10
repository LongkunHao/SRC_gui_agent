import requests

def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()

    issue = next((i for i in state["issues"] if i["id"] == 43), None)
    if issue is None:
        return False, "Issue #43 not found."

    if 3 not in issue["labelIds"]:
        return False, "Issue #43 does not have the documentation label (id 3)."

    return True, "Issue #43 has the documentation label (id 3)."
