import requests

def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()
    match = [i for i in state["issues"] if i["title"] == "Investigate flaky test suite"]
    if not match:
        return False, "Issue 'Investigate flaky test suite' not found."
    issue = match[0]
    if 1 not in issue["labelIds"]:
        return False, "Label 'bug' (id 1) not found on the issue."
    if 7 not in issue["labelIds"]:
        return False, "Label 'backend' (id 7) not found on the issue."
    return True, "Issue 'Investigate flaky test suite' created with correct labels."
