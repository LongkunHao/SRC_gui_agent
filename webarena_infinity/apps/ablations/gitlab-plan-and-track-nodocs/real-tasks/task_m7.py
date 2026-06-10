import requests

def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()

    issue = next((i for i in state["issues"] if i["id"] == 60), None)
    if issue is None:
        return False, "Issue #60 not found."

    if 11 not in issue.get("assigneeIds", []):
        return False, f"David Kim (id 11) not in assigneeIds: {issue.get('assigneeIds', [])}."

    if issue.get("iterationId") != 7:
        return False, f"iterationId is {issue.get('iterationId')}, expected 7 (Sprint 7)."

    return True, "Issue #60 assigned to David Kim with iteration set to Sprint 7."
