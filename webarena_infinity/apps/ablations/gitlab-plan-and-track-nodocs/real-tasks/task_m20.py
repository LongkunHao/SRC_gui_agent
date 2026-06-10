import requests

def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()

    issue78 = next((i for i in state["issues"] if i["id"] == 78), None)
    if issue78 is None:
        return False, "Issue #78 not found."

    if issue78["status"] != "closed":
        return False, f"Issue #78 status is '{issue78['status']}', expected 'closed'."

    rel78 = next((r for r in issue78.get("relatedIssues", []) if r["issueId"] == 31 and r["type"] == "related_to"), None)
    if rel78 is None:
        return False, f"Issue #78 does not have a 'related_to' relation to #31. relatedIssues: {issue78.get('relatedIssues', [])}."

    issue31 = next((i for i in state["issues"] if i["id"] == 31), None)
    if issue31 is None:
        return False, "Issue #31 not found."

    rel31 = next((r for r in issue31.get("relatedIssues", []) if r["issueId"] == 78 and r["type"] == "related_to"), None)
    if rel31 is None:
        return False, f"Issue #31 does not have a 'related_to' relation to #78. relatedIssues: {issue31.get('relatedIssues', [])}."

    return True, "Issue #78 closed with bidirectional 'related_to' link to issue #31."
