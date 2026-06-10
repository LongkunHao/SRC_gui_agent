import requests

def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()
    issue = next((i for i in state["issues"] if i["id"] == 9), None)
    if not issue:
        return False, "Issue #9 not found."
    if 4 in issue["labelIds"]:
        return False, "Label 'performance' (id 4) is still on issue #9."
    return True, "Label 'performance' removed from issue #9 via /unlabel quick action."
