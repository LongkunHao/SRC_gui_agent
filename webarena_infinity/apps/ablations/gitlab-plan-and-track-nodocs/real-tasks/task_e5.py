import requests

def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()

    issue = next((i for i in state["issues"] if i["id"] == 22), None)
    if issue is None:
        return False, "Issue #22 not found."

    if 8 in issue["assigneeIds"]:
        return False, "Emily Okonkwo (id 8) is still assigned to issue #22."

    return True, "Emily Okonkwo (id 8) has been removed from issue #22."
