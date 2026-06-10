# Task: Security audit — revoke old sessions, unused passkeys, unused API keys.
import requests

def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, f"Failed to fetch state: HTTP {resp.status_code}"
    state = resp.json()
    failures = []

    # Today: 2026-03-06. 90 days ago ≈ 2025-12-06
    # Non-current sessions signed in before 2025-12-06:
    #   sess_06 Safari on iPad (2025-11-28) → revoke
    #   sess_08 Edge on Windows (2025-10-15) → revoke
    # Keep: sess_03 (Dec 10), sess_07 (Dec 20), sess_02 (Jan 15), sess_04 (Feb 20), sess_05 (Jan 5)
    sessions = state.get("sessions", [])
    session_names = [s.get("deviceName") for s in sessions]
    for name in ("Safari on iPad", "Edge on Windows"):
        if name in session_names:
            failures.append(f"Session '{name}' should have been revoked (signed in >90 days ago)")
    for name in ("Chrome on macOS", "Safari on iPhone", "Linear Desktop on macOS",
                 "Firefox on Windows", "Chrome on Linux", "Chrome on Android"):
        if name not in session_names:
            failures.append(f"Session '{name}' should remain")

    # Passkeys not used in last 7 days (before 2026-02-27):
    #   YubiKey 5C NFC (lastUsed 2026-02-20) → remove
    # Keep: MacBook (Mar 5), iPhone (Mar 4)
    passkeys = state.get("passkeys", [])
    pk_names = [p.get("name") for p in passkeys]
    if "YubiKey 5C NFC" in pk_names:
        failures.append("YubiKey should have been removed (not used in last 7 days)")
    for name in ("MacBook Pro Touch ID", "iPhone Face ID"):
        if name not in pk_names:
            failures.append(f"Passkey '{name}' should remain")

    # API keys not used in last 7 days (before 2026-02-27):
    #   Mobile App Testing (lastUsed 2026-01-20) → revoke
    # Keep: CI/CD (Mar 6), Slack Bot (Mar 5), Data Export (Feb 28), Monitoring (Mar 6)
    api_keys = state.get("apiKeys", [])
    key_labels = [k.get("label") for k in api_keys]
    if "Mobile App Testing" in key_labels:
        failures.append("'Mobile App Testing' should have been revoked (not used in last 7 days)")
    for label in ("CI/CD Pipeline", "Slack Bot Integration", "Data Export Script", "Monitoring Dashboard"):
        if label not in key_labels:
            failures.append(f"API key '{label}' should remain")

    if failures:
        return False, "; ".join(failures)
    return True, "Security audit completed: old sessions, unused passkeys, and unused API keys removed."
