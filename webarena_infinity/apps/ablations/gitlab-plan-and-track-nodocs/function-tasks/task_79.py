import requests

def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()
    issue16 = next((i for i in state["issues"] if i["id"] == 16), None)
    issue15 = next((i for i in state["issues"] if i["id"] == 15), None)
    if not issue16 or not issue15:
        return False, "Issue #16 or #15 not found."
    rel16 = next((r for r in issue16["relatedIssues"] if r["issueId"] == 15 and r["type"] == "is_blocked_by"), None)
    if not rel16:
        return False, "Issue #16 does not have an 'is_blocked_by' relationship to issue #15."
    rel15 = next((r for r in issue15["relatedIssues"] if r["issueId"] == 16 and r["type"] == "blocks"), None)
    if not rel15:
        return False, "Issue #15 does not have a 'blocks' relationship to issue #16."
    return True, "Issue #16 is_blocked_by issue #15 relationship created."
