import requests

def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."

    state = resp.json()
    issue = next((i for i in state["issues"] if i["id"] == 34), None)
    if not issue:
        return False, "Issue #34 not found."

    # Emily Okonkwo = id 8
    if 8 not in issue["assigneeIds"]:
        return False, "Emily Okonkwo (id 8) is not assigned to issue #34."

    return True, "Emily Okonkwo assigned to issue #34 via quick action."
