import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()

    bug_id = next(l["id"] for l in state["labels"] if l["name"] == "bug")
    feature_id = next(l["id"] for l in state["labels"] if l["name"] == "feature")
    critical_id = next(l["id"] for l in state["labels"] if l["name"] == "priority::critical")
    low_id = next(l["id"] for l in state["labels"] if l["name"] == "priority::low")
    priority_ids = {l["id"] for l in state["labels"] if l["name"].startswith("priority::")}
    v20_id = next(m["id"] for m in state["milestones"] if "v2.0" in m["title"])

    # Bug issues in v2.0 (open): #28, #31, #33, #35, #101, #104
    bug_issues = [28, 31, 33, 35, 101, 104]
    for issue_id in bug_issues:
        issue = next((i for i in state["issues"] if i["id"] == issue_id), None)
        if issue is None:
            return False, f"Issue #{issue_id} not found."
        if critical_id not in issue.get("labelIds", []):
            return False, (
                f"Issue #{issue_id} does not have priority::critical label. "
                f"Labels: {issue.get('labelIds')}."
            )
        other_priority = [l for l in issue.get("labelIds", [])
                          if l in priority_ids and l != critical_id]
        if other_priority:
            return False, (
                f"Issue #{issue_id} has extra priority labels: {other_priority}."
            )

    # Feature issues in v2.0 (open): #73, #76, #102, #113
    feature_issues = [73, 76, 102, 113]
    for issue_id in feature_issues:
        issue = next((i for i in state["issues"] if i["id"] == issue_id), None)
        if issue is None:
            return False, f"Issue #{issue_id} not found."
        if low_id not in issue.get("labelIds", []):
            return False, (
                f"Issue #{issue_id} does not have priority::low label. "
                f"Labels: {issue.get('labelIds')}."
            )
        other_priority = [l for l in issue.get("labelIds", [])
                          if l in priority_ids and l != low_id]
        if other_priority:
            return False, (
                f"Issue #{issue_id} has extra priority labels: {other_priority}."
            )

    return True, "Bug issues set to critical, feature issues set to low in v2.0."
