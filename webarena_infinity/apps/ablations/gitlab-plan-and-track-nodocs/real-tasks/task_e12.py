import requests

def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()

    level = state.get("notificationSettings", {}).get("level")
    if level != "watch":
        return False, f"Notification level is '{level}', expected 'watch'."

    return True, "Notification level is set to 'watch'."
