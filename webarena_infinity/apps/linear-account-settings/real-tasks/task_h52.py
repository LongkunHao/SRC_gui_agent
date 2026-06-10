# Task: Revoke most recently signed-in non-current session and most recently created API key.
import requests

def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, f"Failed to fetch state: HTTP {resp.status_code}"
    state = resp.json()
    failures = []

    # Most recently signed-in non-current: Firefox on Windows (2026-02-20)
    sessions = state.get("sessions", [])
    device_names = [s.get("deviceName") for s in sessions]
    if "Firefox on Windows" in device_names:
        failures.append("'Firefox on Windows' session should have been revoked (most recent non-current sign-in)")

    # Most recently created API key: Mobile App Testing (2026-01-15)
    api_keys = state.get("apiKeys", [])
    labels = [k.get("label") for k in api_keys]
    if "Mobile App Testing" in labels:
        failures.append("'Mobile App Testing' API key should have been revoked (most recently created)")

    if failures:
        return False, "; ".join(failures)
    return True, "Most recent non-current session and most recent API key revoked."
