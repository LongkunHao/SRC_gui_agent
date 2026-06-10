import requests

def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."

    state = resp.json()
    issue28 = next((i for i in state["issues"] if i["id"] == 28), None)
    issue31 = next((i for i in state["issues"] if i["id"] == 31), None)
    if not issue28 or not issue31:
        return False, "Issue #28 or #31 not found."

    rel28 = next((r for r in issue28["relatedIssues"] if r["issueId"] == 31 and r["type"] == "related_to"), None)
    if not rel28:
        return False, "Issue #28 does not have a 'related_to' relationship with issue #31."

    rel31 = next((r for r in issue31["relatedIssues"] if r["issueId"] == 28 and r["type"] == "related_to"), None)
    if not rel31:
        return False, "Issue #31 does not have a 'related_to' relationship with issue #28."

    return True, "Related issue link created between #28 and #31."
