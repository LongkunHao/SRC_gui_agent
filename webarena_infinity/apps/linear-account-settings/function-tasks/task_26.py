import requests

def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()
    if state["preferences"]["desktopNotificationBadge"] == False:
        return True, "Notification badge toggle correctly turned off."
    return False, f"Expected desktopNotificationBadge to be False, got {state['preferences']['desktopNotificationBadge']}."
