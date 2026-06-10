import requests

def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()

    issue14 = next((i for i in state["issues"] if i["id"] == 14), None)
    if issue14 is None:
        return False, "Issue #14 not found."

    issue49 = next((i for i in state["issues"] if i["id"] == 49), None)
    if issue49 is None:
        return False, "Issue #49 not found."

    blocks_entry = next((r for r in issue14.get("relatedIssues", []) if r["issueId"] == 49 and r["type"] == "blocks"), None)
    if blocks_entry is None:
        return False, f"Issue #14 does not have a 'blocks' relation to #49. relatedIssues: {issue14.get('relatedIssues', [])}."

    blocked_entry = next((r for r in issue49.get("relatedIssues", []) if r["issueId"] == 14 and r["type"] == "is_blocked_by"), None)
    if blocked_entry is None:
        return False, f"Issue #49 does not have an 'is_blocked_by' relation to #14. relatedIssues: {issue49.get('relatedIssues', [])}."

    return True, "Issue #14 blocks issue #49 with correct bidirectional relationship."
