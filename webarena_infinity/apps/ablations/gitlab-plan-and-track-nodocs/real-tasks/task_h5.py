import requests

def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()

    milestone = next((m for m in state["milestones"] if m["title"] == "Critical Fixes"), None)
    if milestone is None:
        return False, "Milestone 'Critical Fixes' not found."

    if milestone.get("dueDate") != "2026-04-01":
        return False, f"Milestone 'Critical Fixes' dueDate is '{milestone.get('dueDate')}', expected '2026-04-01'."

    milestone_id = milestone["id"]

    for issue_id in [11, 33, 41]:
        issue = next((i for i in state["issues"] if i["id"] == issue_id), None)
        if issue is None:
            return False, f"Issue #{issue_id} not found."
        if issue.get("milestoneId") != milestone_id:
            return False, f"Issue #{issue_id} milestoneId is {issue.get('milestoneId')}, expected {milestone_id}."

    return True, "Milestone 'Critical Fixes' created with dueDate 2026-04-01 and issues #11, #33, #41 assigned."
