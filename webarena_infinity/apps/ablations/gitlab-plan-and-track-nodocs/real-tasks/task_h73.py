import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()

    # #32 (webhook retry) should block #36 (notification preferences)
    issue32 = next((i for i in state["issues"] if i["id"] == 32), None)
    if issue32 is None:
        return False, "Issue #32 not found."

    has_blocks = any(
        r.get("issueId") == 36 and r.get("type") == "blocks"
        for r in issue32.get("relatedIssues", [])
    )
    if not has_blocks:
        return False, (
            f"Issue #32 does not have a 'blocks' relationship with #36. "
            f"Related: {issue32.get('relatedIssues')}."
        )

    # #36 weight should be 5 + 5 = 10
    issue36 = next((i for i in state["issues"] if i["id"] == 36), None)
    if issue36 is None:
        return False, "Issue #36 not found."
    if issue36.get("weight") != 10:
        return False, (
            f"Issue #36 weight is {issue36.get('weight')}, expected 10 (5 + 5)."
        )

    return True, "Issue #32 blocks #36, and #36 weight is 10."
