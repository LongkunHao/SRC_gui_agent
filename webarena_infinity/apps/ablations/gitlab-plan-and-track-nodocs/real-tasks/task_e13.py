import requests

def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()

    notifications = state.get("notifications", [])
    if not notifications:
        return False, "No notifications found in state."

    unread = [n for n in notifications if n.get("read") is not True]
    if unread:
        return False, f"{len(unread)} notification(s) are still unread."

    return True, "All notifications are marked as read."
