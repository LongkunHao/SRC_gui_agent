import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()

    v21 = next((m for m in state["milestones"] if "v2.1" in m.get("title", "")), None)
    if v21 is None:
        return False, "Milestone 'v2.1' not found."

    medium_label = next((l for l in state["labels"] if l["name"] == "priority::medium"), None)
    low_label = next((l for l in state["labels"] if l["name"] == "priority::low"), None)
    if not medium_label or not low_label:
        return False, "Priority labels not found."
    med_id = medium_label["id"]
    low_id = low_label["id"]

    # Open devops issues from v3.0: #54, #108
    for issue_id in [54, 108]:
        issue = next((i for i in state["issues"] if i["id"] == issue_id), None)
        if issue is None:
            return False, f"Issue #{issue_id} not found."
        if issue.get("milestoneId") != v21["id"]:
            return False, (
                f"Issue #{issue_id} milestoneId is {issue.get('milestoneId')}, "
                f"expected {v21['id']} (v2.1)."
            )
        if med_id not in issue.get("labelIds", []):
            return False, f"Issue #{issue_id} does not have priority::medium label."
        if low_id in issue.get("labelIds", []):
            return False, f"Issue #{issue_id} still has priority::low label."

    return True, "Issues #54, #108 moved to v2.1 with priority::medium."
