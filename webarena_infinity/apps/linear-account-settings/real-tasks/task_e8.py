# Task: Remove the YubiKey passkey.
import requests

def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, f"Failed to fetch state: HTTP {resp.status_code}"
    state = resp.json()
    passkeys = state.get("passkeys", [])
    for p in passkeys:
        if p.get("name") == "YubiKey 5C NFC":
            return False, "YubiKey 5C NFC passkey still exists."
    return True, "YubiKey 5C NFC passkey has been removed."
