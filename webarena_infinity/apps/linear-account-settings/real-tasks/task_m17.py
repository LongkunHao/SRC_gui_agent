# Stop sending urgent email notifications immediately
import requests

def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, f"Failed to fetch state: HTTP {resp.status_code}"
    state = resp.json()
    val = state.get("notificationSettings", {}).get("email", {}).get("sendUrgentImmediately")
    if val is not False:
        return False, f"notificationSettings.email.sendUrgentImmediately is {val}, expected False"
    return True, "Send urgent immediately is disabled"
