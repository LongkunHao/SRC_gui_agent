# Enable desktop cycle update notifications
import requests

def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, f"Failed to fetch state: HTTP {resp.status_code}"
    state = resp.json()
    val = state.get("notificationSettings", {}).get("desktop", {}).get("cycleUpdated")
    if val is not True:
        return False, f"notificationSettings.desktop.cycleUpdated is {val}, expected True"
    return True, "Desktop cycle update notifications are enabled"
