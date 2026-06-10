# Task: Revoke all sessions except the current one.
import requests

def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, f"Failed to fetch state: HTTP {resp.status_code}"
    state = resp.json()
    sessions = state.get("sessions", [])

    if len(sessions) != 1:
        return False, f"Expected exactly 1 session, found {len(sessions)}"
    if not sessions[0].get("isCurrent"):
        return False, "Remaining session does not have isCurrent == True"
    return True, "All non-current sessions revoked."
