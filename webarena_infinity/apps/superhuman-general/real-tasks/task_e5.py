import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()

    desktop = state.get("settings", {}).get("notifications", {}).get("desktop")
    if desktop is False:
        return True, "Desktop notifications are turned off."
    return False, f"Desktop notifications are not turned off (desktop={desktop!r})."
