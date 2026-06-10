import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()

    v20_id = next(m["id"] for m in state["milestones"] if "v2.0" in m["title"])

    # Epic 8 (Enterprise SSO) should have no children
    epic8 = next((e for e in state["epics"] if e["id"] == 8), None)
    if epic8 is None:
        return False, "Epic 'Enterprise SSO Integration' (id 8) not found."
    if epic8.get("childIssueIds"):
        return False, (
            f"Epic 8 still has children: {epic8.get('childIssueIds')}."
        )

    # Epic 1 (User Auth Overhaul) should contain #57, #58, #59
    epic1 = next((e for e in state["epics"] if e["id"] == 1), None)
    if epic1 is None:
        return False, "Epic 'User Authentication Overhaul' (id 1) not found."
    for issue_id in [57, 58, 59]:
        if issue_id not in epic1.get("childIssueIds", []):
            return False, (
                f"Issue #{issue_id} not in epic 1 childIssueIds: "
                f"{epic1.get('childIssueIds')}."
            )

    # Issues #57, #58, #59 should be in v2.0 milestone
    for issue_id in [57, 58, 59]:
        issue = next((i for i in state["issues"] if i["id"] == issue_id), None)
        if issue is None:
            return False, f"Issue #{issue_id} not found."
        if issue.get("milestoneId") != v20_id:
            return False, (
                f"Issue #{issue_id} milestoneId is {issue.get('milestoneId')}, "
                f"expected {v20_id} (v2.0)."
            )

    return True, "SSO children moved to Auth epic with v2.0 milestone."
