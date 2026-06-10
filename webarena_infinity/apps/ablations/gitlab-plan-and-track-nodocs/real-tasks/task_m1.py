import requests

def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()

    issue = next((i for i in state["issues"] if i["title"] == "Implement GraphQL subscriptions for real-time updates"), None)
    if issue is None:
        return False, "Issue with title 'Implement GraphQL subscriptions for real-time updates' not found."

    if issue["status"] != "open":
        return False, f"Issue status is '{issue['status']}', expected 'open'."

    if 7 not in issue["assigneeIds"]:
        return False, f"Li Wei (id 7) not in assigneeIds: {issue['assigneeIds']}."

    if 7 not in issue["labelIds"]:
        return False, f"Label 'backend' (id 7) not in labelIds: {issue['labelIds']}."

    if 2 not in issue["labelIds"]:
        return False, f"Label 'feature' (id 2) not in labelIds: {issue['labelIds']}."

    if issue.get("milestoneId") != 4:
        return False, f"milestoneId is {issue.get('milestoneId')}, expected 4."

    if issue.get("weight") != 8:
        return False, f"weight is {issue.get('weight')}, expected 8."

    return True, "Issue 'Implement GraphQL subscriptions for real-time updates' created correctly with all required attributes."
