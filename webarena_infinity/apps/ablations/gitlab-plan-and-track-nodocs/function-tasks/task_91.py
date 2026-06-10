import requests

def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()
    match = [i for i in state["iterations"] if i["title"] == "Sprint 3"]
    if match:
        return False, "Iteration 'Sprint 3' still exists."
    for issue in state["issues"]:
        if issue.get("iterationId") == 3:
            return False, f"Issue #{issue['id']} still references iteration id 3."
    return True, "Iteration 'Sprint 3' deleted and references cleaned up."
