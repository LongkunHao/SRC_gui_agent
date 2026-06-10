import requests

def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."

    state = resp.json()
    issue = next((i for i in state["issues"] if i["id"] == 9), None)
    if not issue:
        return False, "Issue #9 not found."

    # Original timeSpent is 7200. Adding 2h (7200) = 14400
    if issue["timeSpent"] < 14400:
        return False, f"Issue #9 timeSpent is {issue['timeSpent']}, expected at least 14400 (original 7200 + 7200 added)."

    return True, "Issue #9 time spent updated (2 hours added)."
