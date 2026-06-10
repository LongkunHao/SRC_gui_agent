import requests

def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()

    issue = next((i for i in state["issues"] if i["id"] == 42), None)
    if issue is None:
        return False, "Issue #42 not found."

    if 6 not in issue.get("assigneeIds", []):
        return False, f"Tom Ramirez (id 6) not in assigneeIds: {issue.get('assigneeIds', [])}."

    if 11 not in issue.get("assigneeIds", []):
        return False, f"David Kim (id 11) not in assigneeIds: {issue.get('assigneeIds', [])}."

    if 12 not in issue.get("labelIds", []):
        return False, f"Label 'priority::high' (id 12) not in labelIds: {issue.get('labelIds', [])}."

    if 13 in issue.get("labelIds", []):
        return False, "Label 'priority::medium' (id 13) should not be in labelIds but is still present."

    return True, "Issue #42 has Tom and David assigned with high priority and no medium priority."
