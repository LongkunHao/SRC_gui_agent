# Task: Disable desktop notifications.
import requests

def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, f"Failed to fetch state: HTTP {resp.status_code}"
    state = resp.json()
    enabled = state.get("notificationSettings", {}).get("desktop", {}).get("enabled")
    if enabled is False:
        return True, "Desktop notifications are disabled."
    return False, f"Expected desktop notifications enabled to be False, got {enabled}."
