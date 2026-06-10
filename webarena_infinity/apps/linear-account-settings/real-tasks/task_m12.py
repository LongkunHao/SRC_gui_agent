# Disconnect the GitLab account
import requests

def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, f"Failed to fetch state: HTTP {resp.status_code}"
    state = resp.json()
    accounts = state.get("connectedAccounts", [])
    providers = [a.get("provider") for a in accounts]
    if "GitLab" in providers:
        return False, "GitLab account is still connected"
    return True, "GitLab account has been disconnected"
