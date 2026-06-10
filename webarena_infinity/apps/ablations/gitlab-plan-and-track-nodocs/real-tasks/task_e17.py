import requests

def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()

    issue = next((i for i in state["issues"] if i["id"] == 23), None)
    if issue is None:
        return False, "Issue #23 not found."

    if issue["timeEstimate"] != 144000:
        return False, f"Issue #23 time estimate is {issue['timeEstimate']}, expected 144000 (40 hours)."

    return True, "Issue #23 time estimate is 144000 seconds (40 hours)."
