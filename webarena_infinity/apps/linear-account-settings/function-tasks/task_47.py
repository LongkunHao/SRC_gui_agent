import requests

def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()
    for session in state["sessions"]:
        if session.get("deviceName") == "Safari on iPhone":
            return False, "Session 'Safari on iPhone' still exists."
    return True, "Session 'Safari on iPhone' successfully revoked."
