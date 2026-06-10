import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()

    epic = next((e for e in state["epics"] if "Mobile Responsive Redesign" in e.get("title", "")), None)
    if epic is None:
        return False, "Epic 'Mobile Responsive Redesign' not found."

    medium_label = next((l for l in state["labels"] if l["name"] == "priority::medium"), None)
    if medium_label is None:
        return False, "Label 'priority::medium' not found."
    mid = medium_label["id"]

    # Issues #15 and #16 had priority::medium and were open children
    for issue_id in [15, 16]:
        issue = next((i for i in state["issues"] if i["id"] == issue_id), None)
        if issue is None:
            return False, f"Issue #{issue_id} not found."
        if issue["status"] != "closed":
            return False, f"Issue #{issue_id} status is '{issue['status']}', expected 'closed'."
        if issue_id in epic.get("childIssueIds", []):
            return False, f"Issue #{issue_id} still in epic childIssueIds: {epic['childIssueIds']}."

    return True, "Issues #15, #16 closed and removed from Mobile Responsive Redesign epic."
