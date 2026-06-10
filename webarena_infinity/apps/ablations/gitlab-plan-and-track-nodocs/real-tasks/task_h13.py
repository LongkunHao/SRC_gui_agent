import requests

def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()

    issue20 = next((i for i in state["issues"] if i["id"] == 20), None)
    if issue20 is None:
        return False, "Issue #20 not found."

    issue21 = next((i for i in state["issues"] if i["id"] == 21), None)
    if issue21 is None:
        return False, "Issue #21 not found."

    # Check #20 blocks #21
    blocks_entry = next((r for r in issue20.get("relatedIssues", []) if r.get("issueId") == 21 and r.get("type") == "blocks"), None)
    if blocks_entry is None:
        return False, f"Issue #20 does not have a 'blocks' relationship with issue #21. Related: {issue20.get('relatedIssues')}."

    # Check #21 is_blocked_by #20
    blocked_entry = next((r for r in issue21.get("relatedIssues", []) if r.get("issueId") == 20 and r.get("type") == "is_blocked_by"), None)
    if blocked_entry is None:
        return False, f"Issue #21 does not have an 'is_blocked_by' relationship with issue #20. Related: {issue21.get('relatedIssues')}."

    # Check #20 has priority::high and not priority::medium
    if 12 not in issue20.get("labelIds", []):
        return False, f"Label priority::high (id 12) not in issue #20 labelIds: {issue20.get('labelIds')}."
    if 13 in issue20.get("labelIds", []):
        return False, f"Label priority::medium (id 13) still in issue #20 labelIds: {issue20.get('labelIds')}."

    # Check #21 has priority::high
    if 12 not in issue21.get("labelIds", []):
        return False, f"Label priority::high (id 12) not in issue #21 labelIds: {issue21.get('labelIds')}."

    return True, "Issue #20 blocks #21 with correct relationship entries, both have priority::high."
