import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()

    # Issue #2 is blocked by issue #1.
    # Issue #1 has assigneeIds [4, 7] and weight 8.
    issue2 = next((i for i in state["issues"] if i["id"] == 2), None)
    if issue2 is None:
        return False, "Issue #2 not found."

    # Check assignees: should include both 4 and 7
    for uid in [4, 7]:
        if uid not in issue2.get("assigneeIds", []):
            return False, (
                f"User {uid} not in issue #2 assigneeIds: "
                f"{issue2.get('assigneeIds')}."
            )

    if issue2.get("weight") != 8:
        return False, (
            f"Issue #2 weight is {issue2.get('weight')}, expected 8 "
            f"(matching blocking issue #1)."
        )

    return True, "Issue #2 has blocker's assignees [4, 7] and weight 8."
