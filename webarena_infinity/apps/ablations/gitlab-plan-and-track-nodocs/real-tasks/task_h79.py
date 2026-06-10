import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()

    sprint7 = next(
        (it for it in state["iterations"] if it.get("title") == "Sprint 7"), None
    )
    if sprint7 is None:
        return False, "Sprint 7 not found."
    s7_id = sprint7["id"]

    # Open issues with frontend label (8) in Sprint 6 (current): #15, #22, #28, #31, #78
    for issue_id in [15, 22, 28, 31, 78]:
        issue = next((i for i in state["issues"] if i["id"] == issue_id), None)
        if issue is None:
            return False, f"Issue #{issue_id} not found."
        if issue.get("iterationId") != s7_id:
            return False, (
                f"Issue #{issue_id} iterationId is {issue.get('iterationId')}, "
                f"expected {s7_id} (Sprint 7)."
            )

    return True, "Frontend issues moved from Sprint 6 to Sprint 7."
