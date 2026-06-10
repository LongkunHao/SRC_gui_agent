import requests

def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()

    for issue_id in [60, 61, 62]:
        issue = next((i for i in state["issues"] if i["id"] == issue_id), None)
        if issue is None:
            return False, f"Issue #{issue_id} not found."
        if 11 not in issue.get("assigneeIds", []):
            return False, f"David Kim (id 11) not in assigneeIds for issue #{issue_id}: {issue.get('assigneeIds')}."
        if issue.get("iterationId") != 7:
            return False, f"Issue #{issue_id} iterationId is {issue.get('iterationId')}, expected 7."

    return True, "Issues #60, #61, #62 all have David Kim assigned and iterationId 7."
