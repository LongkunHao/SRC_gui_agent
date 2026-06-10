import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()

    # Priya Sharma (id 5) authored the most comments (5).
    priya_id = 5

    # Open children of User Authentication Overhaul epic: #1, #2, #3, #45, #46
    for issue_id in [1, 2, 3, 45, 46]:
        issue = next((i for i in state["issues"] if i["id"] == issue_id), None)
        if issue is None:
            return False, f"Issue #{issue_id} not found."
        if priya_id not in issue.get("assigneeIds", []):
            return False, (
                f"Priya Sharma (id {priya_id}) not in issue #{issue_id} "
                f"assigneeIds: {issue.get('assigneeIds')}."
            )

    return True, "Priya Sharma assigned to all open Auth Overhaul epic children."
