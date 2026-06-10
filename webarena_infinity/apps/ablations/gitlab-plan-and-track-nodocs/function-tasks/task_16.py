import requests

def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."

    state = resp.json()
    issue = next((i for i in state["issues"] if i["title"] == "Add GraphQL support for API v3"), None)
    if not issue:
        return False, "Issue 'Add GraphQL support for API v3' not found."

    # Tom Ramirez = id 6
    if 6 not in issue["assigneeIds"]:
        return False, "Tom Ramirez (id 6) is not assigned to the issue."

    # backend = id 7, feature = id 2
    if 7 not in issue["labelIds"]:
        return False, "Label 'backend' (id 7) not found on the issue."
    if 2 not in issue["labelIds"]:
        return False, "Label 'feature' (id 2) not found on the issue."

    # v2.1 — Integrations = milestone id 4
    if issue["milestoneId"] != 4:
        return False, f"Milestone is {issue['milestoneId']}, expected 4 (v2.1 — Integrations)."

    if issue["weight"] != 8:
        return False, f"Weight is {issue['weight']}, expected 8."

    return True, "Issue 'Add GraphQL support for API v3' created with correct fields."
