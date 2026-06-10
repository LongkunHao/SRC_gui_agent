# Task: Remove least recently used passkey, disconnect most recently connected SCM,
# revoke Windows 10 session.
import requests

def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, f"Failed to fetch state: HTTP {resp.status_code}"
    state = resp.json()
    failures = []

    # Least recently used passkey: YubiKey 5C NFC (lastUsedAt 2026-02-20)
    passkeys = state.get("passkeys", [])
    pk_names = [p.get("name") for p in passkeys]
    if "YubiKey 5C NFC" in pk_names:
        failures.append("'YubiKey 5C NFC' still present (least recently used passkey)")

    # Most recently connected SCM: GitLab (2024-08-22 vs GitHub 2024-06-16)
    accounts = state.get("connectedAccounts", [])
    providers = [a.get("provider") for a in accounts]
    if "GitLab" in providers:
        failures.append("'GitLab' still connected (most recently connected SCM)")
    if "GitHub" not in providers:
        failures.append("'GitHub' was incorrectly disconnected")

    # Windows 10 session: Edge on Windows (os: Windows 10)
    sessions = state.get("sessions", [])
    win10_sessions = [s for s in sessions if "Windows 10" in s.get("os", "")]
    if win10_sessions:
        failures.append("Windows 10 session still present")

    if failures:
        return False, "; ".join(failures)
    return True, "Least used passkey removed, most recent SCM disconnected, Windows 10 session revoked."
