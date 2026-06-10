import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()

    # Current Design Cycle = Design Cycle 4 (cadenceId 2, status 'current')
    dc4 = next(
        (it for it in state["iterations"]
         if it.get("cadenceId") == 2 and it.get("status") == "current"),
        None,
    )
    if dc4 is None:
        return False, "No current Design Cycle iteration found."

    dc4_id = dc4["id"]

    # Open Accessibility Compliance children: #22, #23, #55
    for issue_id in [22, 23, 55]:
        issue = next((i for i in state["issues"] if i["id"] == issue_id), None)
        if issue is None:
            return False, f"Issue #{issue_id} not found."
        if issue.get("iterationId") != dc4_id:
            return False, (
                f"Issue #{issue_id} iterationId is {issue.get('iterationId')}, "
                f"expected {dc4_id} (current Design Cycle)."
            )
        if issue.get("weight") != 5:
            return False, f"Issue #{issue_id} weight is {issue.get('weight')}, expected 5."

    return True, "Issues #22, #23, #55 set to current Design Cycle with weight 5."
