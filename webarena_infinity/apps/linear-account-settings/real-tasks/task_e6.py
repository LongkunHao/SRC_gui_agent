# Task: Stop receiving changelog notifications.
import requests

def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, f"Failed to fetch state: HTTP {resp.status_code}"
    state = resp.json()
    val = state.get("notificationSettings", {}).get("receiveChangelogs")
    if val is False:
        return True, "receiveChangelogs is disabled."
    return False, f"Expected receiveChangelogs to be False, got {val}."
