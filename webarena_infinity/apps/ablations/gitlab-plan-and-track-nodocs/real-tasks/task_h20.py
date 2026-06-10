import requests

def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()

    notif_epic = next((e for e in state["epics"] if e.get("title") == "Notification System Revamp"), None)
    if notif_epic is None:
        return False, "Epic 'Notification System Revamp' not found."

    if notif_epic.get("status") != "closed":
        return False, f"Epic 'Notification System Revamp' status is '{notif_epic.get('status')}', expected 'closed'."

    for issue_id in [63, 64, 65]:
        if issue_id in notif_epic.get("childIssueIds", []):
            return False, f"Issue #{issue_id} still in 'Notification System Revamp' childIssueIds."

    search_epic = next((e for e in state["epics"] if e.get("title") == "Search Infrastructure Upgrade"), None)
    if search_epic is None:
        return False, "Epic 'Search Infrastructure Upgrade' not found."

    for issue_id in [63, 64, 65]:
        if issue_id not in search_epic.get("childIssueIds", []):
            return False, f"Issue #{issue_id} not in 'Search Infrastructure Upgrade' childIssueIds: {search_epic.get('childIssueIds')}."

    return True, "Notification System Revamp closed, children #63, #64, #65 moved to Search Infrastructure Upgrade."
