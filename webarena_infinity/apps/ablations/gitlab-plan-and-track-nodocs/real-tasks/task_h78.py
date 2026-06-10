import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()

    sarah_id = 1
    ni_id = next(l["id"] for l in state["labels"] if l["name"] == "needs-investigation")
    v30_id = next(m["id"] for m in state["milestones"] if "v3.0" in m["title"])

    # Open issues in v3.0 Enterprise milestone
    target_ids = [
        46, 52, 54, 57, 58, 59, 71, 95, 100, 106, 108, 109, 118, 119, 128, 130
    ]

    for issue_id in target_ids:
        issue = next((i for i in state["issues"] if i["id"] == issue_id), None)
        if issue is None:
            return False, f"Issue #{issue_id} not found."
        if sarah_id not in issue.get("assigneeIds", []):
            return False, (
                f"Sarah Chen (id {sarah_id}) not in issue #{issue_id} "
                f"assigneeIds: {issue.get('assigneeIds')}."
            )
        if ni_id not in issue.get("labelIds", []):
            return False, (
                f"Issue #{issue_id} missing needs-investigation label. "
                f"Labels: {issue.get('labelIds')}."
            )

    return True, "Sarah Chen assigned and needs-investigation added to all v3.0 issues."
