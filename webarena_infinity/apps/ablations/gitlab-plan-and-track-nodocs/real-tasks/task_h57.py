import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()

    epic = next((e for e in state["epics"] if e.get("title") == "Frontend Modernization"), None)
    if epic is None:
        return False, "Epic 'Frontend Modernization' not found."

    frontend_label = next((l for l in state["labels"] if l["name"] == "frontend"), None)
    ux_label = next((l for l in state["labels"] if l["name"] == "UX"), None)
    if not frontend_label or not ux_label:
        return False, "frontend or UX label not found."

    if frontend_label["id"] not in epic.get("labels", []):
        return False, f"Epic missing frontend label. Labels: {epic.get('labels')}."
    if ux_label["id"] not in epic.get("labels", []):
        return False, f"Epic missing UX label. Labels: {epic.get('labels')}."

    # Unassigned open Backlog issues with frontend label: #34, #70, #103, #116, #122
    expected = [34, 70, 103, 116, 122]
    for issue_id in expected:
        if issue_id not in epic.get("childIssueIds", []):
            return False, (
                f"Issue #{issue_id} not in epic childIssueIds: {epic.get('childIssueIds')}."
            )

    return True, f"Epic 'Frontend Modernization' created with children {expected}."
