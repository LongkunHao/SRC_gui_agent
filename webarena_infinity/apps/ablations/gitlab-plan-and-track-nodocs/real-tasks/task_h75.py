import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()

    # Open Backlog (milestone 6) issues with weight 1: #72, #120, #127, #129
    for issue_id in [72, 120, 127, 129]:
        issue = next((i for i in state["issues"] if i["id"] == issue_id), None)
        if issue is None:
            return False, f"Issue #{issue_id} not found."
        if issue.get("status") != "closed":
            return False, (
                f"Issue #{issue_id} status is '{issue.get('status')}', expected 'closed'."
            )
        if issue.get("assigneeIds"):
            return False, (
                f"Issue #{issue_id} still has assignees: {issue.get('assigneeIds')}."
            )

    return True, "Weight-1 Backlog issues closed with assignees cleared."
