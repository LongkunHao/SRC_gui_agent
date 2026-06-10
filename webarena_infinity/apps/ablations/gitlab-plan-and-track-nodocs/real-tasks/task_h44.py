import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()

    # Open breaking-change issues in v2.0 with no time spent: #8, #10, #47
    for issue_id in [8, 10, 47]:
        issue = next((i for i in state["issues"] if i["id"] == issue_id), None)
        if issue is None:
            return False, f"Issue #{issue_id} not found."
        if issue.get("timeEstimate") != 86400:
            return False, (
                f"Issue #{issue_id} timeEstimate is {issue.get('timeEstimate')}, "
                f"expected 86400 (24 hours)."
            )

    return True, "Issues #8, #10, #47 all have timeEstimate of 86400 (24h)."
