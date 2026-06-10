import requests

def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."

    state = resp.json()
    issue = next((i for i in state["issues"] if i["id"] == 9), None)
    if not issue:
        return False, "Issue #9 not found."

    # breaking-change = label id 20
    if 20 not in issue["labelIds"]:
        return False, "Label 'breaking-change' (id 20) not found on issue #9."

    return True, "Label 'breaking-change' added to issue #9 via quick action."
