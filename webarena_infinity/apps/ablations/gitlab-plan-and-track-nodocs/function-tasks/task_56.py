import requests

def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."

    state = resp.json()
    settings = state.get("notificationSettings", {})
    if settings.get("level") != "on_mention":
        return False, f"Notification level is '{settings.get('level')}', expected 'on_mention'."

    return True, "Notification settings level changed to 'on_mention'."
