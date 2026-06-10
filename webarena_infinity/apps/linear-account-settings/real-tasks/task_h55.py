# Task: Revoke all sessions not from same city as current session.
import requests

def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, f"Failed to fetch state: HTTP {resp.status_code}"
    state = resp.json()
    failures = []

    # Current session is in San Francisco. Keep only San Francisco sessions.
    # Keep: sess_01 (current, SF), sess_02 (SF), sess_03 (SF), sess_06 (SF)
    # Revoke: sess_04 (New York), sess_05 (Austin), sess_07 (Los Angeles), sess_08 (Seattle)
    sessions = state.get("sessions", [])
    for s in sessions:
        loc = s.get("location", "")
        if "San Francisco" not in loc:
            failures.append(f"Session from '{loc}' should have been revoked (not San Francisco)")

    # Should still have San Francisco sessions
    sf_sessions = [s for s in sessions if "San Francisco" in s.get("location", "")]
    if len(sf_sessions) < 2:
        failures.append(f"Expected at least 2 San Francisco sessions remaining, got {len(sf_sessions)}")

    if failures:
        return False, "; ".join(failures)
    return True, "All non-San Francisco sessions revoked."
