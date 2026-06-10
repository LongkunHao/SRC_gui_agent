import requests

def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()

    issue = next((i for i in state["issues"] if i["id"] == 2), None)
    if issue is None:
        return False, "Issue #2 not found."

    if issue.get("timeEstimate") != 216000:
        return False, f"timeEstimate is {issue.get('timeEstimate')}, expected 216000 (60h)."

    if issue.get("timeSpent") != 36000:
        return False, f"timeSpent is {issue.get('timeSpent')}, expected 36000 (10h)."

    return True, "Issue #2 time tracking updated to 60h estimate (216000s) and 10h spent (36000s)."
