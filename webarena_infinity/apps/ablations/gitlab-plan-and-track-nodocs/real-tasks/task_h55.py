import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()

    sprint7 = next(
        (it for it in state["iterations"] if it.get("title") == "Sprint 7"),
        None,
    )
    if sprint7 is None:
        return False, "Iteration 'Sprint 7' not found."

    s7_id = sprint7["id"]

    # Sprint 8 should be deleted
    sprint8 = next(
        (it for it in state["iterations"] if it.get("title") == "Sprint 8"),
        None,
    )
    if sprint8 is not None:
        return False, "Sprint 8 still exists — should have been deleted."

    # Issues that were in Sprint 8: #10, #17, #20, #21, #42, #47, #48, #49, #53
    for issue_id in [10, 17, 20, 21, 42, 47, 48, 49, 53]:
        issue = next((i for i in state["issues"] if i["id"] == issue_id), None)
        if issue is None:
            return False, f"Issue #{issue_id} not found."
        if issue.get("iterationId") != s7_id:
            return False, (
                f"Issue #{issue_id} iterationId is {issue.get('iterationId')}, "
                f"expected {s7_id} (Sprint 7)."
            )

    return True, "Sprint 8 deleted, all its issues moved to Sprint 7."
