import requests

def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()
    issue = next((i for i in state["issues"] if i["id"] == 28), None)
    if not issue:
        return False, "Issue #28 not found."
    if issue["weight"] is not None:
        return False, f"Issue #28 weight is {issue['weight']}, expected None."
    return True, "Issue #28 weight cleared successfully."
