import requests

def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()

    issue = next((i for i in state["issues"] if i["id"] == 9), None)
    if issue is None:
        return False, "Issue #9 not found."

    if issue["weight"] != 8:
        return False, f"Issue #9 weight is {issue['weight']}, expected 8."

    return True, "Issue #9 weight is 8."
