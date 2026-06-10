# Revoke the Data Export Script and Slack Bot Integration API keys
import requests

def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, f"Failed to fetch state: HTTP {resp.status_code}"
    state = resp.json()
    keys = state.get("apiKeys", [])
    labels = [k.get("label") for k in keys]
    if "Data Export Script" in labels:
        return False, "Data Export Script API key still exists"
    if "Slack Bot Integration" in labels:
        return False, "Slack Bot Integration API key still exists"
    return True, "Both Data Export Script and Slack Bot Integration API keys have been revoked"
