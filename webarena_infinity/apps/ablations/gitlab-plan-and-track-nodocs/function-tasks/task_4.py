import requests

def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."

    state = resp.json()
    issue = next((i for i in state["issues"] if i["id"] == 29), None)
    if not issue:
        return False, "Issue #29 not found."

    expected = "Avatar upload fails for large PNG files"
    if issue["title"] != expected:
        return False, f"Issue #29 title is '{issue['title']}', expected '{expected}'."

    return True, "Issue #29 title updated successfully."
