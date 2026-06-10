# Revoke the session from the Linux machine
import requests

def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, f"Failed to fetch state: HTTP {resp.status_code}"
    state = resp.json()
    sessions = state.get("sessions", [])
    device_names = [s.get("deviceName") for s in sessions]
    if "Chrome on Linux" in device_names:
        return False, "Chrome on Linux session still exists"
    return True, "Chrome on Linux session has been revoked"
