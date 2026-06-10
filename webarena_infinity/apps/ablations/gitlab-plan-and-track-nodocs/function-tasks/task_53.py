import requests

def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."

    state = resp.json()
    # Backlog = milestone id 6
    for issue_id in [66, 96, 98]:
        issue = next((i for i in state["issues"] if i["id"] == issue_id), None)
        if not issue:
            return False, f"Issue #{issue_id} not found."
        if issue["milestoneId"] != 6:
            return False, f"Issue #{issue_id} milestoneId is {issue['milestoneId']}, expected 6 (Backlog)."

    return True, "Issues #66, #96, and #98 milestone set to Backlog."
