import requests

def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()

    issue = next((i for i in state["issues"] if i["id"] == 29), None)
    if issue is None:
        return False, "Issue #29 not found."

    if issue.get("milestoneId") != 3:
        return False, f"Issue #29 milestoneId is {issue.get('milestoneId')}, expected 3 (v2.0)."

    if 12 not in issue.get("labelIds", []):
        return False, f"Label 'priority::high' (id 12) not in labelIds: {issue.get('labelIds', [])}."

    if 13 in issue.get("labelIds", []):
        return False, f"Label 'priority::medium' (id 13) should not be in labelIds but is still present."

    return True, "Issue #29 moved to v2.0 milestone with high priority label and medium priority removed."
