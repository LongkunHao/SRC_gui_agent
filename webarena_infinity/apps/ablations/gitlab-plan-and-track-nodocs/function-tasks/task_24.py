import requests

def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."

    state = resp.json()
    issue = next((i for i in state["issues"] if i["id"] == 72), None)
    if not issue:
        return False, "Issue #72 not found."

    if issue["weight"] != 5:
        return False, f"Issue #72 weight is {issue['weight']}, expected 5."

    return True, "Issue #72 weight set to 5 via quick action."
