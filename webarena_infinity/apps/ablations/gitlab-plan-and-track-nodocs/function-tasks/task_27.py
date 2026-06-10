import requests

def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."

    state = resp.json()
    issue = next((i for i in state["issues"] if i["id"] == 3), None)
    if not issue:
        return False, "Issue #3 not found."

    # Original timeSpent = 21600. /spend 3h30m adds 12600 (3*3600 + 30*60). Total = 34200
    if issue["timeSpent"] < 34200:
        return False, f"Issue #3 timeSpent is {issue['timeSpent']}, expected at least 34200 (original 21600 + 12600 from /spend 3h30m)."

    return True, "Issue #3 time spent updated via /spend 3h30m quick action."
