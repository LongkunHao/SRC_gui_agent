import requests

def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()

    issue = next((i for i in state["issues"] if i["id"] == 34), None)
    if issue is None:
        return False, "Issue #34 not found."

    if issue.get("milestoneId") != 4:
        return False, f"milestoneId is {issue.get('milestoneId')}, expected 4 (v2.1)."

    if 5 not in issue.get("assigneeIds", []):
        return False, f"Priya Sharma (id 5) not in assigneeIds: {issue.get('assigneeIds', [])}."

    return True, "Issue #34 moved to v2.1 milestone and assigned to Priya Sharma."
