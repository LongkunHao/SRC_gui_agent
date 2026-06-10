# Task: Revoke the Mobile App Testing API key.
import requests

def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, f"Failed to fetch state: HTTP {resp.status_code}"
    state = resp.json()
    api_keys = state.get("apiKeys", [])
    for key in api_keys:
        if key.get("label") == "Mobile App Testing":
            return False, "Mobile App Testing API key still exists"
    return True, "Mobile App Testing API key has been revoked"
