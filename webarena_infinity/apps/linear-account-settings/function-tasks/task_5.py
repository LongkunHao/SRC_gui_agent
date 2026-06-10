import requests

def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()
    for account in state.get("connectedAccounts", []):
        if account.get("provider") == "GitHub":
            return False, "GitHub account is still connected."
    return True, "GitHub account successfully disconnected."
