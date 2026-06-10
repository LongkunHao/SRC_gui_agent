import requests

def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()

    epic = next((e for e in state["epics"] if e.get("title") == "Platform Stability"), None)
    if epic is None:
        return False, "Epic 'Platform Stability' not found."

    if 4 not in epic.get("labels", []):
        return False, f"Label 'performance' (id 4) not in epic labels: {epic.get('labels')}."

    if 12 not in epic.get("labels", []):
        return False, f"Label 'priority::high' (id 12) not in epic labels: {epic.get('labels')}."

    for issue_id in [11, 33, 41]:
        if issue_id not in epic.get("childIssueIds", []):
            return False, f"Issue #{issue_id} not in epic childIssueIds: {epic.get('childIssueIds')}."

    return True, "Epic 'Platform Stability' created with performance and priority::high labels, and issues #11, #33, #41 as children."
