import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()

    # Emily Okonkwo (id 8) open issues in Backlog (milestone 6):
    # #37, #67, #72, #98, #110, #120
    for issue_id in [37, 67, 72, 98, 110, 120]:
        issue = next((i for i in state["issues"] if i["id"] == issue_id), None)
        if issue is None:
            return False, f"Issue #{issue_id} not found."
        if issue.get("status") != "closed":
            return False, (
                f"Issue #{issue_id} status is '{issue.get('status')}', expected 'closed'."
            )
        if issue.get("weight") != 1:
            return False, (
                f"Issue #{issue_id} weight is {issue.get('weight')}, expected 1."
            )

    return True, "Emily's Backlog issues closed with weight 1."
