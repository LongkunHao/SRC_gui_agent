# Task: Revoke sessions from Texas and New York, create passkey named after current session's city.
import requests

def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, f"Failed to fetch state: HTTP {resp.status_code}"
    state = resp.json()
    failures = []

    # Austin, TX (sess_05) and New York, NY (sess_04) should be revoked
    sessions = state.get("sessions", [])
    for s in sessions:
        loc = s.get("location", "")
        if "Austin" in loc or "New York" in loc:
            failures.append(f"Session from '{loc}' should have been revoked")

    # Current session is in San Francisco — passkey named "San Francisco"
    passkeys = state.get("passkeys", [])
    pk_names = [p.get("name") for p in passkeys]
    if "San Francisco" not in pk_names:
        failures.append("Expected a passkey named 'San Francisco'")

    if failures:
        return False, "; ".join(failures)
    return True, "Texas and New York sessions revoked; passkey 'San Francisco' created."
