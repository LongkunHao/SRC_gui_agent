import requests

def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."

    state = resp.json()
    iteration = next((i for i in state["iterations"] if i["title"] == "Sprint 8"), None)
    if iteration:
        return False, "Iteration 'Sprint 8' still exists."

    # Side effect: issues with iterationId 8 should be cleared
    issue10 = next((i for i in state["issues"] if i["id"] == 10), None)
    if issue10 and issue10["iterationId"] == 8:
        return False, "Issue #10 still references deleted iteration."

    return True, "Iteration 'Sprint 8' deleted and references cleared."
