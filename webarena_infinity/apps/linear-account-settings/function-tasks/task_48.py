import requests

def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()
    for session in state["sessions"]:
        if session.get("deviceName") == "Firefox on Windows":
            return False, "Session 'Firefox on Windows' still exists."
    return True, "Session 'Firefox on Windows' successfully revoked."
