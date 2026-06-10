import requests

def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()

    for issue_id in [19, 20, 21, 42, 50, 53]:
        issue = next((i for i in state["issues"] if i["id"] == issue_id), None)
        if issue is None:
            return False, f"Issue #{issue_id} not found."
        if 3 not in issue.get("assigneeIds", []):
            return False, f"Ana Garcia (id 3) not in assigneeIds for issue #{issue_id}: {issue.get('assigneeIds')}."
        if 6 in issue.get("assigneeIds", []):
            return False, f"Tom Ramirez (id 6) still in assigneeIds for issue #{issue_id}: {issue.get('assigneeIds')}."

    return True, "Tom's v2.1 issues reassigned to Ana Garcia successfully."
