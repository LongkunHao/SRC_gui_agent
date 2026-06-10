import requests

def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."

    state = resp.json()
    epic = next((e for e in state["epics"] if e["title"] == "User Authentication Overhaul"), None)
    if not epic:
        return False, "Epic 'User Authentication Overhaul' not found."

    if 45 in epic["childIssueIds"]:
        return False, "Issue #45 is still in epic's child issues."

    return True, "Issue #45 removed from epic 'User Authentication Overhaul'."
