# Remove the iPhone Face ID passkey
import requests

def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, f"Failed to fetch state: HTTP {resp.status_code}"
    state = resp.json()
    passkeys = state.get("passkeys", [])
    names = [p.get("name") for p in passkeys]
    if "iPhone Face ID" in names:
        return False, "iPhone Face ID passkey still exists"
    return True, "iPhone Face ID passkey has been removed"
