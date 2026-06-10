# Task: Create a new API key labeled 'Staging Environment'.
import requests

def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, f"Failed to fetch state: HTTP {resp.status_code}"
    state = resp.json()
    api_keys = state.get("apiKeys", [])
    for key in api_keys:
        if key.get("label") == "Staging Environment":
            return True, "API key 'Staging Environment' found."
    return False, f"No API key with label 'Staging Environment' found. Keys: {[k.get('label') for k in api_keys]}"
