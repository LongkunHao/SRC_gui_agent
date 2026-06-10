import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()

    # Check Sprint 9 exists in Engineering Sprints cadence (cadenceId 1)
    sprint9 = next(
        (it for it in state["iterations"]
         if "Sprint 9" in it.get("title", "") and it.get("cadenceId") == 1),
        None,
    )
    if sprint9 is None:
        return False, "Iteration 'Sprint 9' in Engineering Sprints cadence not found."

    if sprint9.get("startDate") != "2026-04-28":
        return False, f"Sprint 9 startDate is '{sprint9.get('startDate')}', expected '2026-04-28'."

    if sprint9.get("endDate") != "2026-05-11":
        return False, f"Sprint 9 endDate is '{sprint9.get('endDate')}', expected '2026-05-11'."

    s9_id = sprint9["id"]

    # Issues #42 and #53 (devops-labeled in Sprint 8) should now be in Sprint 9
    for issue_id in [42, 53]:
        issue = next((i for i in state["issues"] if i["id"] == issue_id), None)
        if issue is None:
            return False, f"Issue #{issue_id} not found."
        if issue.get("iterationId") != s9_id:
            return False, (
                f"Issue #{issue_id} iterationId is {issue.get('iterationId')}, "
                f"expected {s9_id} (Sprint 9)."
            )

    return True, "Sprint 9 created and devops issues #42, #53 moved into it."
