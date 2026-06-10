import requests

def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."

    state = resp.json()
    issue = next((i for i in state["issues"] if i["id"] == 29), None)
    if not issue:
        return False, "Issue #29 not found."

    # needs-investigation label id = 19
    if 19 not in issue["labelIds"]:
        return False, "Label 'needs-investigation' (id 19) not found on issue #29."

    return True, "Label 'needs-investigation' added to issue #29."
