# Task: Disconnect the Figma account.
import requests

def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, f"Failed to fetch state: HTTP {resp.status_code}"
    state = resp.json()
    connected = state.get("connectedAccounts", [])
    for acct in connected:
        if acct.get("provider") == "Figma":
            return False, "Figma account is still connected"
    return True, "Figma account has been disconnected"
