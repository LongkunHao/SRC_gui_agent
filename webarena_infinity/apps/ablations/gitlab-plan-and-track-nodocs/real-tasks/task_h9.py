import requests

def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()

    for issue_id in [37, 67, 72, 110, 120]:
        issue = next((i for i in state["issues"] if i["id"] == issue_id), None)
        if issue is None:
            return False, f"Issue #{issue_id} not found."
        if issue.get("iterationId") != 7:
            return False, f"Issue #{issue_id} iterationId is {issue.get('iterationId')}, expected 7."

    return True, "Emily's unassigned-iteration bugs (#37, #67, #72, #110, #120) all set to Sprint 7."
