# Task: Turn off the open in desktop app setting.
import requests

def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, f"Failed to fetch state: HTTP {resp.status_code}"
    state = resp.json()
    val = state.get("preferences", {}).get("openInDesktopApp")
    if val is False:
        return True, "Open in desktop app is disabled"
    return False, f"openInDesktopApp is {val}, expected False"
