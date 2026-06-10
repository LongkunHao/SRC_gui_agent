# Task: Revoke the sessions from all mobile devices.
import requests

def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, f"Failed to fetch state: HTTP {resp.status_code}"
    state = resp.json()
    sessions = state.get("sessions", [])

    mobile_sessions = [s for s in sessions if s.get("deviceType") == "mobile"]
    if mobile_sessions:
        names = [s.get("name", "unknown") for s in mobile_sessions]
        return False, f"Found {len(mobile_sessions)} mobile session(s) still present: {names}"

    if len(sessions) == 0:
        return False, "All sessions were removed, but only mobile sessions should have been revoked."

    return True, "All mobile sessions revoked successfully."
