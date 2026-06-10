# Task: Revoke the non-current session signed in longest ago and the one signed in most recently.
import requests

def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, f"Failed to fetch state: HTTP {resp.status_code}"
    state = resp.json()
    failures = []

    sessions = state.get("sessions", [])
    session_names = [s.get("deviceName") for s in sessions]

    # Earliest sign-in (non-current): Edge on Windows (2025-10-15)
    if "Edge on Windows" in session_names:
        failures.append("'Edge on Windows' still present (earliest sign-in)")

    # Most recent sign-in (non-current): Firefox on Windows (2026-02-20)
    if "Firefox on Windows" in session_names:
        failures.append("'Firefox on Windows' still present (most recent sign-in)")

    # Other sessions should remain
    remaining_count = len(sessions)
    if remaining_count < 5:
        failures.append(f"Too many sessions revoked: only {remaining_count} remain (expected 6)")

    if failures:
        return False, "; ".join(failures)
    return True, "Sessions with earliest and most recent sign-in dates revoked."
