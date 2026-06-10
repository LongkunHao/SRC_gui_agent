# Task: Register a new passkey called 'Windows Hello'.
import requests

def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, f"Failed to fetch state: HTTP {resp.status_code}"
    state = resp.json()
    passkeys = state.get("passkeys", [])
    for pk in passkeys:
        if pk.get("name") == "Windows Hello":
            return True, "Passkey 'Windows Hello' found."
    return False, f"No passkey with name 'Windows Hello' found. Passkeys: {[p.get('name') for p in passkeys]}"
