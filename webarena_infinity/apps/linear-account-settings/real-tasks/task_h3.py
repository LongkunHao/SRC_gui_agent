# Task: Disconnect all source code integrations (GitHub and GitLab).
import requests

def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, f"Failed to fetch state: HTTP {resp.status_code}"
    state = resp.json()
    accounts = state.get("connectedAccounts", [])
    providers = [a.get("provider") for a in accounts]

    if "GitHub" in providers:
        return False, "GitHub is still connected"
    if "GitLab" in providers:
        return False, "GitLab is still connected"
    return True, "GitHub and GitLab disconnected."
