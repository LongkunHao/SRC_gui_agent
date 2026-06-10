# Task: Disable mobile notifications entirely.
import requests

def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, f"Failed to fetch state: HTTP {resp.status_code}"
    state = resp.json()
    mobile_enabled = state.get("notificationSettings", {}).get("mobile", {}).get("enabled")
    if mobile_enabled is not False:
        return False, f"Expected mobile notifications enabled == False, got {mobile_enabled}"
    return True, "Mobile notifications disabled successfully."
