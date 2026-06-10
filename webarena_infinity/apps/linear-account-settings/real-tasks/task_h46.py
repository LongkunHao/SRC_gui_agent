# Task: Add passkey named after longest-connected provider, remove least-recently-used passkey.
import requests

def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, f"Failed to fetch state: HTTP {resp.status_code}"
    state = resp.json()
    failures = []

    # Longest connected: Google (2024-06-15). Passkey name = "Google"
    passkeys = state.get("passkeys", [])
    pk_names = [p.get("name") for p in passkeys]
    if "Google" not in pk_names:
        failures.append("Expected a passkey named 'Google'")

    # Least recently used passkey: YubiKey 5C NFC (last used 2026-02-20)
    if "YubiKey 5C NFC" in pk_names:
        failures.append("YubiKey 5C NFC passkey should have been removed (least recently used)")

    if failures:
        return False, "; ".join(failures)
    return True, "Passkey 'Google' added and YubiKey 5C NFC removed."
