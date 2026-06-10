import requests

def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()
    sessions = state["sessions"]
    if len(sessions) != 1:
        return False, f"Expected exactly 1 session remaining, found {len(sessions)}."
    if not sessions[0].get("isCurrent"):
        return False, "The remaining session is not marked as current."
    return True, "All sessions except current successfully revoked."
