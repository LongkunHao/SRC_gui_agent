import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()

    # Highest weight in current sprint (Sprint 6) is issue #41 (weight 13).
    # timeEstimate=36000, timeSpent was 25200, remaining=10800.
    # After logging remaining: timeSpent should be 36000.
    issue = next((i for i in state["issues"] if i["id"] == 41), None)
    if issue is None:
        return False, "Issue #41 not found."

    if issue["status"] != "closed":
        return False, f"Issue #41 status is '{issue['status']}', expected 'closed'."

    if issue.get("timeSpent") != 36000:
        return False, (
            f"Issue #41 timeSpent is {issue.get('timeSpent')}, expected 36000 "
            f"(original 25200 + remaining 10800)."
        )

    return True, "Issue #41 closed with all remaining time logged (timeSpent=36000)."
