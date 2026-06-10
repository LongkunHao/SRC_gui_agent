import requests

def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()

    issue = next((i for i in state["issues"] if i["title"] == "Update Redis client library to v5"), None)
    if issue is None:
        return False, "Issue with title 'Update Redis client library to v5' not found."

    if 7 not in issue.get("labelIds", []):
        return False, f"Label 'backend' (id 7) not in labelIds: {issue.get('labelIds')}."

    if 10 not in issue.get("labelIds", []):
        return False, f"Label 'tech-debt' (id 10) not in labelIds: {issue.get('labelIds')}."

    if 13 not in issue.get("labelIds", []):
        return False, f"Label 'priority::medium' (id 13) not in labelIds: {issue.get('labelIds')}."

    if 5 not in issue.get("assigneeIds", []):
        return False, f"Priya (id 5) not in assigneeIds: {issue.get('assigneeIds')}."

    if 11 not in issue.get("assigneeIds", []):
        return False, f"David Kim (id 11) not in assigneeIds: {issue.get('assigneeIds')}."

    if issue.get("weight") != 13:
        return False, f"Issue weight is {issue.get('weight')}, expected 13."

    if issue.get("milestoneId") != 3:
        return False, f"Issue milestoneId is {issue.get('milestoneId')}, expected 3."

    return True, "Issue 'Update Redis client library to v5' created correctly with all required attributes."
