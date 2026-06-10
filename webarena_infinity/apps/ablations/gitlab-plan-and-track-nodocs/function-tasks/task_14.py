import requests

def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."

    state = resp.json()
    issue = next((i for i in state["issues"] if i["id"] == 31), None)
    if not issue:
        return False, "Issue #31 not found."

    # 4 hours = 14400 seconds
    if issue["timeEstimate"] != 14400:
        return False, f"Issue #31 timeEstimate is {issue['timeEstimate']}, expected 14400 (4h)."

    return True, "Issue #31 time estimate set to 4 hours."
