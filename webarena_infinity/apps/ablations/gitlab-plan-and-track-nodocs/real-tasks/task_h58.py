import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()

    # The only closed epic is Data Export & Reporting (id 7)
    epic = next(
        (e for e in state["epics"] if "Data Export" in e.get("title", "")),
        None,
    )
    if epic is None:
        return False, "Epic 'Data Export & Reporting' not found."

    if epic["status"] != "open":
        return False, f"Epic status is '{epic['status']}', expected 'open' (reopened)."

    david_id = 11  # David Kim
    for issue_id in [25, 26, 27]:
        issue = next((i for i in state["issues"] if i["id"] == issue_id), None)
        if issue is None:
            return False, f"Issue #{issue_id} not found."
        if david_id not in issue.get("assigneeIds", []):
            return False, (
                f"David Kim (id {david_id}) not in issue #{issue_id} "
                f"assigneeIds: {issue.get('assigneeIds')}."
            )

    return True, "Epic reopened and David Kim assigned to issues #25, #26, #27."
