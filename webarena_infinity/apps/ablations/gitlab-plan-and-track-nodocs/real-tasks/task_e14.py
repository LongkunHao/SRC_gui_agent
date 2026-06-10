import requests

def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()

    issue = next((i for i in state["issues"] if i["id"] == 111), None)
    if issue is None:
        return False, "Issue #111 not found."

    if 2 not in issue["assigneeIds"]:
        return False, "Marek Kowalski (id 2) is not assigned to issue #111."

    return True, "Marek Kowalski (id 2) is assigned to issue #111."
