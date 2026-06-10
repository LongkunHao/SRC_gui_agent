import requests

def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."

    state = resp.json()
    # Priya Sharma = id 5
    for issue_id in [34, 68, 70]:
        issue = next((i for i in state["issues"] if i["id"] == issue_id), None)
        if not issue:
            return False, f"Issue #{issue_id} not found."
        if 5 not in issue["assigneeIds"]:
            return False, f"Priya Sharma (id 5) not assigned to issue #{issue_id}."

    return True, "Issues #34, #68, and #70 bulk assigned to Priya Sharma."
