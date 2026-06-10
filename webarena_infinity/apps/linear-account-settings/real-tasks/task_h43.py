# Task: Revoke all non-Apple-OS sessions, remove cross-platform passkey.
import requests

def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, f"Failed to fetch state: HTTP {resp.status_code}"
    state = resp.json()
    failures = []

    # Apple OS sessions to keep: macOS (sess_01 current, sess_03), iOS (sess_02), iPadOS (sess_06)
    # Non-Apple to revoke: Windows 11 (sess_04), Ubuntu (sess_05), Android (sess_07), Windows 10 (sess_08)
    sessions = state.get("sessions", [])
    for s in sessions:
        os_name = s.get("os", "")
        if not any(apple in os_name for apple in ("macOS", "iOS", "iPadOS")):
            failures.append(f"Session with OS '{os_name}' should have been revoked")

    # Cross-platform passkey: YubiKey 5C NFC
    passkeys = state.get("passkeys", [])
    for p in passkeys:
        if p.get("credentialType") == "cross-platform":
            failures.append(f"Cross-platform passkey '{p.get('name')}' should have been removed")

    if failures:
        return False, "; ".join(failures)
    return True, "Non-Apple sessions revoked and cross-platform passkey removed."
