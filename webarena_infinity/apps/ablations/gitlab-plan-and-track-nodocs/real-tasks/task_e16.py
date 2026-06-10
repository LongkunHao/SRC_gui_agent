import requests

def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()

    issue = next((i for i in state["issues"] if i["id"] == 55), None)
    if issue is None:
        return False, "Issue #55 not found."

    if issue["milestoneId"] != 4:
        return False, f"Issue #55 milestoneId is {issue['milestoneId']}, expected 4 (v2.1)."

    return True, "Issue #55 milestone is set to v2.1 (id 4)."
