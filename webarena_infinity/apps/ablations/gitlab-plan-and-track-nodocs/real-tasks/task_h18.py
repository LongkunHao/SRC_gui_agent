import requests

def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()

    for issue_id in [32, 45, 125, 129]:
        issue = next((i for i in state["issues"] if i["id"] == issue_id), None)
        if issue is None:
            return False, f"Issue #{issue_id} not found."
        if issue.get("timeSpent") != 14400:
            return False, f"Issue #{issue_id} timeSpent is {issue.get('timeSpent')}, expected 14400 (4h)."

    return True, "Li Wei's no-time-spent issues (#32, #45, #125, #129) each have timeSpent of 14400 (4h)."
