# Task: Revoke the session from the Firefox on Windows device.
import requests

def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, f"Failed to fetch state: HTTP {resp.status_code}"
    state = resp.json()
    sessions = state.get("sessions", [])
    for s in sessions:
        if s.get("deviceName") == "Firefox on Windows":
            return False, "Session 'Firefox on Windows' still exists."
    return True, "Firefox on Windows session successfully revoked."
