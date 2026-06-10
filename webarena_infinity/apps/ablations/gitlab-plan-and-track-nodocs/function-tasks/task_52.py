import requests

def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."

    state = resp.json()
    # tech-debt = label id 10
    for issue_id in [29, 37]:
        issue = next((i for i in state["issues"] if i["id"] == issue_id), None)
        if not issue:
            return False, f"Issue #{issue_id} not found."
        if 10 not in issue["labelIds"]:
            return False, f"Label 'tech-debt' (id 10) not found on issue #{issue_id}."

    return True, "Label 'tech-debt' added to issues #29 and #37."
