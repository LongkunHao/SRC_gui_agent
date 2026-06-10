import requests

def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."

    state = resp.json()
    unread = [n for n in state["notifications"] if n["read"] is not True]
    if unread:
        return False, f"{len(unread)} notifications are still unread."

    return True, "All notifications marked as read."
