import requests

def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()

    epic = next((e for e in state["epics"] if e["title"] == "Notification System Revamp"), None)
    if epic is None:
        return False, "Epic with title 'Notification System Revamp' not found."

    child_ids = epic.get("childIssueIds", [])

    if 94 not in child_ids:
        return False, f"Issue #94 not in childIssueIds: {child_ids}."

    if 115 not in child_ids:
        return False, f"Issue #115 not in childIssueIds: {child_ids}."

    return True, "Epic 'Notification System Revamp' has child issues #94 and #115."
