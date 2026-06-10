# Task: Revoke sessions signed in before 2026, disable mobile, add passkey 'Post-Cleanup Key'.
import requests

def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, f"Failed to fetch state: HTTP {resp.status_code}"
    state = resp.json()
    failures = []

    # Sessions signed in before 2026: sess_03 (Dec 2025), sess_06 (Nov 2025),
    # sess_07 (Dec 2025), sess_08 (Oct 2025)
    sessions = state.get("sessions", [])
    for s in sessions:
        signed_in = s.get("signedInAt", "")
        if signed_in < "2026-01-01" and not s.get("isCurrent"):
            failures.append(f"Session '{s.get('deviceName')}' signed in {signed_in} should be revoked")

    # Mobile disabled
    mobile = state.get("notificationSettings", {}).get("mobile", {})
    if mobile.get("enabled") is not False:
        failures.append("Mobile notifications should be disabled")

    # Passkey 'Post-Cleanup Key' added
    passkeys = state.get("passkeys", [])
    pk_names = [p.get("name") for p in passkeys]
    if "Post-Cleanup Key" not in pk_names:
        failures.append("Expected a passkey named 'Post-Cleanup Key'")

    if failures:
        return False, "; ".join(failures)
    return True, "Pre-2026 sessions revoked, mobile disabled, passkey added."
