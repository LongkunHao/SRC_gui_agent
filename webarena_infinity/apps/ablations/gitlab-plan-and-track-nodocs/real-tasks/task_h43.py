import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()

    # Full-text search UI issue (#62) is blocked by #61.
    # So #61 is the issue that blocks #62.
    issue = next((i for i in state["issues"] if i["id"] == 61), None)
    if issue is None:
        return False, "Issue #61 not found."

    devops_label = next((l for l in state["labels"] if l["name"] == "devops"), None)
    if devops_label is None:
        return False, "Label 'devops' not found."

    if devops_label["id"] not in issue.get("labelIds", []):
        return False, f"Issue #61 does not have devops label. Labels: {issue.get('labelIds')}."

    if 5 not in issue.get("assigneeIds", []):
        return False, f"Priya Sharma (id 5) not in issue #61 assigneeIds: {issue.get('assigneeIds')}."

    v2_milestone = next((m for m in state["milestones"] if "v2.0" in m.get("title", "")), None)
    if v2_milestone is None:
        return False, "Milestone 'v2.0' not found."

    if issue.get("milestoneId") != v2_milestone["id"]:
        return False, f"Issue #61 milestoneId is {issue.get('milestoneId')}, expected {v2_milestone['id']}."

    return True, "Issue #61 has devops label, Priya Sharma assigned, and v2.0 milestone."
