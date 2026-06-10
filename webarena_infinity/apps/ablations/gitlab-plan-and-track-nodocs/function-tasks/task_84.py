import requests

def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()
    issue = next((i for i in state["issues"] if i["id"] == 52), None)
    if not issue:
        return False, "Issue #52 not found."
    if 9 not in issue["labelIds"]:
        return False, "Label 'devops' (id 9) not found on issue #52."
    if 10 not in issue["labelIds"]:
        return False, "Label 'tech-debt' (id 10) not found on issue #52."
    return True, "Labels 'devops' and 'tech-debt' added to issue #52."
