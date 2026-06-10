import requests

def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."

    state = resp.json()
    issue = next((i for i in state["issues"] if i["id"] == 30), None)
    if not issue:
        return False, "Issue #30 not found."

    # Sprint 7 = iteration id 7
    if issue["iterationId"] != 7:
        return False, f"Issue #30 iterationId is {issue['iterationId']}, expected 7 (Sprint 7)."

    return True, "Issue #30 assigned to iteration Sprint 7."
