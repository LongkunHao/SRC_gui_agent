import requests

def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()

    for issue_id in [19, 20, 21, 53, 54]:
        issue = next((i for i in state["issues"] if i["id"] == issue_id), None)
        if issue is None:
            return False, f"Issue #{issue_id} not found."
        if issue["status"] != "closed":
            return False, f"Issue #{issue_id} status is '{issue['status']}', expected 'closed'."

    epic = next((e for e in state["epics"] if "CI/CD Pipeline Modernization" in e.get("title", "")), None)
    if epic is None:
        return False, "Epic containing 'CI/CD Pipeline Modernization' not found."

    if epic.get("status") != "closed":
        return False, f"Epic 'CI/CD Pipeline Modernization' status is '{epic.get('status')}', expected 'closed'."

    return True, "CI/CD Pipeline Modernization epic and all children (#19, #20, #21, #53, #54) are closed."
