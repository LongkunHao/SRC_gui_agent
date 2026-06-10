import requests

def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."

    state = resp.json()
    issue12 = next((i for i in state["issues"] if i["id"] == 12), None)
    issue49 = next((i for i in state["issues"] if i["id"] == 49), None)
    if not issue12 or not issue49:
        return False, "Issue #12 or #49 not found."

    # Check issue #12 blocks #49
    rel12 = next((r for r in issue12["relatedIssues"] if r["issueId"] == 49 and r["type"] == "blocks"), None)
    if not rel12:
        return False, "Issue #12 does not have a 'blocks' relationship to issue #49."

    # Check reverse: issue #49 is_blocked_by #12
    rel49 = next((r for r in issue49["relatedIssues"] if r["issueId"] == 12 and r["type"] == "is_blocked_by"), None)
    if not rel49:
        return False, "Issue #49 does not have an 'is_blocked_by' relationship to issue #12."

    return True, "Issue #12 blocks issue #49 relationship created."
