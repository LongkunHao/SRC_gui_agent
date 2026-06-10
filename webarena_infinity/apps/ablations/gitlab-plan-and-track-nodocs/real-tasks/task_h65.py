import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()

    # Priya Sharma (id 5) is assigned to the most issues in Sprint 6 (6 issues).
    priya_id = 5

    # Unassigned open issues with priority::high (label 12): #57, #60, #63
    for issue_id in [57, 60, 63]:
        issue = next((i for i in state["issues"] if i["id"] == issue_id), None)
        if issue is None:
            return False, f"Issue #{issue_id} not found."
        if priya_id not in issue.get("assigneeIds", []):
            return False, (
                f"Priya Sharma (id {priya_id}) not in issue #{issue_id} "
                f"assigneeIds: {issue.get('assigneeIds')}."
            )

    return True, "Priya Sharma assigned to unassigned high-priority issues #57, #60, #63."
