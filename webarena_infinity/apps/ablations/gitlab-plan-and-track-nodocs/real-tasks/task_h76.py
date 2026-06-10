import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()

    # Open children of Mobile Responsive Redesign (epic 4): #15, #16, #17, #51, #52
    for issue_id in [15, 16, 17, 51, 52]:
        issue = next((i for i in state["issues"] if i["id"] == issue_id), None)
        if issue is None:
            return False, f"Issue #{issue_id} not found."
        if issue.get("dueDate") != "2026-06-30":
            return False, (
                f"Issue #{issue_id} dueDate is '{issue.get('dueDate')}', "
                f"expected '2026-06-30'."
            )

    epic4 = next((e for e in state["epics"] if e["id"] == 4), None)
    if epic4 is None:
        return False, "Epic 'Mobile Responsive Redesign' (id 4) not found."
    if epic4.get("dueDate") != "2026-07-31":
        return False, (
            f"Epic 4 dueDate is '{epic4.get('dueDate')}', expected '2026-07-31'."
        )

    return True, "Mobile epic children due 2026-06-30, epic due 2026-07-31."
