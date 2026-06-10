# Turn off delay low-priority email notifications outside work hours
import requests

def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, f"Failed to fetch state: HTTP {resp.status_code}"
    state = resp.json()
    val = state.get("notificationSettings", {}).get("email", {}).get("delayLowPriorityOutsideHours")
    if val is not False:
        return False, f"notificationSettings.email.delayLowPriorityOutsideHours is {val}, expected False"
    return True, "Delay low-priority outside hours setting is disabled"
