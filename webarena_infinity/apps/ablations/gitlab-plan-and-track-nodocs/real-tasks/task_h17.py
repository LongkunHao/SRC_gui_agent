import requests

def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()

    epic = next((e for e in state["epics"] if e.get("title") == "Q2 Bug Fixes"), None)
    if epic is None:
        return False, "Epic 'Q2 Bug Fixes' not found."

    if 1 not in epic.get("labels", []):
        return False, f"Label 'bug' (id 1) not in epic labels: {epic.get('labels')}."

    if 12 not in epic.get("labels", []):
        return False, f"Label 'priority::high' (id 12) not in epic labels: {epic.get('labels')}."

    expected_children = [28, 31, 33, 35, 41, 78, 101, 104]
    for issue_id in expected_children:
        if issue_id not in epic.get("childIssueIds", []):
            return False, f"Issue #{issue_id} not in epic childIssueIds: {epic.get('childIssueIds')}."

    return True, "Epic 'Q2 Bug Fixes' created with bug and priority::high labels, and all v2.0 bug issues as children."
