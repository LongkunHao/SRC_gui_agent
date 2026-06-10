import requests

def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."

    state = resp.json()
    issue = next((i for i in state["issues"] if i["id"] == 32), None)
    if not issue:
        return False, "Issue #32 not found."

    # 8h = 28800 seconds
    if issue["timeEstimate"] != 28800:
        return False, f"Issue #32 timeEstimate is {issue['timeEstimate']}, expected 28800 (8h)."

    return True, "Issue #32 time estimate set to 8h via quick action."
