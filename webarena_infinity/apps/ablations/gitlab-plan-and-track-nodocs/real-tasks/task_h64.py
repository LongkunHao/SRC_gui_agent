import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()

    bc_id = next(l["id"] for l in state["labels"] if l["name"] == "breaking-change")
    v21_id = next(m["id"] for m in state["milestones"] if "v2.1" in m["title"])

    # Open children of API v3 Migration (epic 2) with breaking-change: #7, #8, #10, #47
    for issue_id in [7, 8, 10, 47]:
        issue = next((i for i in state["issues"] if i["id"] == issue_id), None)
        if issue is None:
            return False, f"Issue #{issue_id} not found."
        if issue.get("milestoneId") != v21_id:
            return False, (
                f"Issue #{issue_id} milestoneId is {issue.get('milestoneId')}, "
                f"expected {v21_id} (v2.1)."
            )
        if bc_id in issue.get("labelIds", []):
            return False, (
                f"Issue #{issue_id} still has breaking-change label."
            )

    return True, "Issues #7, #8, #10, #47 moved to v2.1 with breaking-change removed."
