# Task: Revoke weekday-signed-in sessions, register passkey named after account creation day.
import requests

def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, f"Failed to fetch state: HTTP {resp.status_code}"
    state = resp.json()
    failures = []

    # Non-current sessions signed in on weekdays:
    #   sess_02 Safari on iPhone (2026-01-15 = Thursday) → revoke
    #   sess_03 Linear Desktop (2025-12-10 = Wednesday) → revoke
    #   sess_04 Firefox on Windows (2026-02-20 = Friday) → revoke
    #   sess_05 Chrome on Linux (2026-01-05 = Monday) → revoke
    #   sess_06 Safari on iPad (2025-11-28 = Friday) → revoke
    #   sess_08 Edge on Windows (2025-10-15 = Wednesday) → revoke
    # Keep: sess_01 (current, Sunday), sess_07 Chrome on Android (2025-12-20 = Saturday)
    sessions = state.get("sessions", [])
    session_names = [s.get("deviceName") for s in sessions]

    should_be_revoked = [
        "Safari on iPhone", "Linear Desktop on macOS", "Firefox on Windows",
        "Chrome on Linux", "Safari on iPad", "Edge on Windows"
    ]
    for name in should_be_revoked:
        if name in session_names:
            failures.append(f"Session '{name}' should have been revoked (signed in on a weekday)")

    should_remain = ["Chrome on macOS", "Chrome on Android"]
    for name in should_remain:
        if name not in session_names:
            failures.append(f"Session '{name}' should remain (signed in on a weekend)")

    # Account created 2024-06-15 = Saturday → passkey named "Saturday"
    passkeys = state.get("passkeys", [])
    pk_names = [p.get("name") for p in passkeys]
    if "Saturday" not in pk_names:
        failures.append("Expected a passkey named 'Saturday' (account created on Saturday)")

    if failures:
        return False, "; ".join(failures)
    return True, "Weekday sessions revoked and passkey 'Saturday' registered."
