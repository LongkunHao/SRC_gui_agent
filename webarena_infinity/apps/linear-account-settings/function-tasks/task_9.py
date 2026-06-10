import requests

def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()
    for account in state.get("connectedAccounts", []):
        if account.get("provider") == "Google":
            return False, "Google account is still connected."
    return True, "Google account successfully disconnected."
