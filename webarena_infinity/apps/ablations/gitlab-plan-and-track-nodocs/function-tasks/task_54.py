import requests

def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."

    state = resp.json()
    notif = next((n for n in state["notifications"] if n["id"] == 1), None)
    if not notif:
        return False, "Notification #1 not found."

    if notif["read"] is not True:
        return False, f"Notification #1 read is {notif['read']}, expected True."

    return True, "Notification #1 marked as read."
