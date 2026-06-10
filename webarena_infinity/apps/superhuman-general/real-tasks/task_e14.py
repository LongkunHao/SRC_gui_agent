import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()

    sound = state.get("settings", {}).get("notifications", {}).get("sound")
    if sound is False:
        return True, "Sound notifications are turned off."
    return False, f"Sound notifications are not turned off (sound={sound!r})."
