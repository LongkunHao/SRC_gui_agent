import requests

def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()
    issue = next((i for i in state["issues"] if i["id"] == 30), None)
    if not issue:
        return False, "Issue #30 not found."
    expected = "Implement dark mode with system preference detection and manual toggle."
    if issue["description"] != expected:
        return False, f"Description not updated correctly. Got: '{issue['description'][:80]}...'"
    return True, "Issue #30 description updated successfully."
