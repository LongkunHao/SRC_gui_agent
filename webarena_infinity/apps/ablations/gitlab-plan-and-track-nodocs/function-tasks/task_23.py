import requests

def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."

    state = resp.json()
    issue = next((i for i in state["issues"] if i["id"] == 28), None)
    if not issue:
        return False, "Issue #28 not found."

    # Backlog = milestone id 6
    if issue["milestoneId"] != 6:
        return False, f"Issue #28 milestoneId is {issue['milestoneId']}, expected 6 (Backlog)."

    return True, "Issue #28 milestone changed to Backlog via quick action."
