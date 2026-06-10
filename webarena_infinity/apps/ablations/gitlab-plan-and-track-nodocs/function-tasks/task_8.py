import requests

def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."

    state = resp.json()
    issue = next((i for i in state["issues"] if i["id"] == 1), None)
    if not issue:
        return False, "Issue #1 not found."

    # priority::high label id = 12
    if 12 in issue["labelIds"]:
        return False, "Label 'priority::high' (id 12) is still on issue #1."

    return True, "Label 'priority::high' removed from issue #1."
