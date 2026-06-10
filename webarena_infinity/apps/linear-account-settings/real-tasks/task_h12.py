# Task: Remove all passkeys from the account.
import requests

def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, f"Failed to fetch state: HTTP {resp.status_code}"
    state = resp.json()
    passkeys = state.get("passkeys", [])

    if len(passkeys) != 0:
        names = [p.get("name", "unknown") for p in passkeys]
        return False, f"Expected 0 passkeys, found {len(passkeys)}: {names}"
    return True, "All passkeys removed."
