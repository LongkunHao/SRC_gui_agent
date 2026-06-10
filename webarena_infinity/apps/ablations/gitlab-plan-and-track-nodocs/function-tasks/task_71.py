import requests

def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()
    match = [i for i in state["issues"] if i["title"] == "Sprint 7 planning notes"]
    if not match:
        return False, "Issue 'Sprint 7 planning notes' not found."
    issue = match[0]
    if issue["iterationId"] != 7:
        return False, f"Iteration is {issue['iterationId']}, expected 7 (Sprint 7)."
    return True, "Issue 'Sprint 7 planning notes' created with Sprint 7 iteration."
