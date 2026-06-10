import requests

def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()

    issue = next((i for i in state["issues"] if i["title"] == "API v3 rate limiting documentation"), None)
    if issue is None:
        return False, "Issue with title 'API v3 rate limiting documentation' not found."

    if issue.get("type") != "task":
        return False, f"Issue type is '{issue.get('type')}', expected 'task'."

    if 7 not in issue.get("assigneeIds", []):
        return False, f"Li Wei (id 7) not in assigneeIds: {issue.get('assigneeIds')}."

    if 3 not in issue.get("labelIds", []):
        return False, f"Label 'documentation' (id 3) not in labelIds: {issue.get('labelIds')}."

    if issue.get("milestoneId") != 3:
        return False, f"milestoneId is {issue.get('milestoneId')}, expected 3."

    return True, "Issue 'API v3 rate limiting documentation' created correctly with type task, Li Wei assigned, documentation label, and milestone 3."
