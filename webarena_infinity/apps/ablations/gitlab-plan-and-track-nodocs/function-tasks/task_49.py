import requests

def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."

    state = resp.json()
    issue1 = next((i for i in state["issues"] if i["id"] == 1), None)
    issue2 = next((i for i in state["issues"] if i["id"] == 2), None)
    if not issue1 or not issue2:
        return False, "Issue #1 or #2 not found."

    rel1 = next((r for r in issue1["relatedIssues"] if r["issueId"] == 2), None)
    if rel1:
        return False, "Issue #1 still has a related issue link to #2."

    rel2 = next((r for r in issue2["relatedIssues"] if r["issueId"] == 1), None)
    if rel2:
        return False, "Issue #2 still has a related issue link to #1."

    return True, "Related issue link between #1 and #2 removed."
