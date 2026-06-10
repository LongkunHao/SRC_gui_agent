# Task: Opt in to product update communications.
import requests

def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, f"Failed to fetch state: HTTP {resp.status_code}"
    state = resp.json()
    val = state.get("notificationSettings", {}).get("receiveProductUpdates")
    if val is True:
        return True, "Product update communications are enabled"
    return False, f"receiveProductUpdates is {val}, expected True"
