import requests

def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()
    match = [m for m in state["milestones"] if m["title"] == "Backlog"]
    if match:
        return False, "Milestone 'Backlog' still exists."
    for issue in state["issues"]:
        if issue.get("milestoneId") == 6:
            return False, f"Issue #{issue['id']} still references milestone id 6."
    return True, "Milestone 'Backlog' deleted and references cleaned up."
