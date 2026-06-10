import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()

    ana_id = 3

    # Only confidential epic = Enterprise SSO Integration (id 8)
    epic8 = next((e for e in state["epics"] if e["id"] == 8), None)
    if epic8 is None:
        return False, "Epic 'Enterprise SSO Integration' (id 8) not found."

    if epic8.get("startDate") != "2026-04-01":
        return False, (
            f"Epic 8 startDate is '{epic8.get('startDate')}', expected '2026-04-01'."
        )

    # Children: #57, #58, #59 — all should have Ana Garcia (3) assigned
    for issue_id in [57, 58, 59]:
        issue = next((i for i in state["issues"] if i["id"] == issue_id), None)
        if issue is None:
            return False, f"Issue #{issue_id} not found."
        if ana_id not in issue.get("assigneeIds", []):
            return False, (
                f"Ana Garcia (id {ana_id}) not in issue #{issue_id} "
                f"assigneeIds: {issue.get('assigneeIds')}."
            )

    return True, "Confidential epic start date set, Ana Garcia assigned to children."
