import requests

def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()

    v11_milestone = next((m for m in state["milestones"] if "v1.1" in m.get("title", "")), None)
    if v11_milestone is not None:
        return False, f"Milestone containing 'v1.1' still exists: '{v11_milestone['title']}'."

    for issue_id in [39, 40, 69, 75, 90, 91, 92, 93, 107]:
        issue = next((i for i in state["issues"] if i["id"] == issue_id), None)
        if issue is None:
            return False, f"Issue #{issue_id} not found."
        if issue.get("milestoneId") != 1:
            return False, f"Issue #{issue_id} milestoneId is {issue.get('milestoneId')}, expected 1 (v1.0)."

    return True, "v1.1 milestone deleted and all its issues moved to v1.0."
