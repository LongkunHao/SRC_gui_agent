import requests

def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()
    epic = next((e for e in state["epics"] if e["title"] == "Notification System Revamp"), None)
    if not epic:
        return False, "Epic 'Notification System Revamp' not found."
    if 66 not in epic["childIssueIds"]:
        return False, "Issue #66 not found in epic 'Notification System Revamp' child issues."
    return True, "Issue #66 added to epic 'Notification System Revamp'."
