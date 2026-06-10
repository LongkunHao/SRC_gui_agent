# Task: Turn off the desktop app notification badge.
import requests

def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, f"Failed to fetch state: HTTP {resp.status_code}"
    state = resp.json()
    val = state.get("preferences", {}).get("desktopNotificationBadge")
    if val is False:
        return True, "Desktop notification badge is disabled"
    return False, f"desktopNotificationBadge is {val}, expected False"
