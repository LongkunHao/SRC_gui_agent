import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()

    settings = state.get("settings", {})

    # Check dark mode
    theme = settings.get("theme", "")
    if theme != "dark":
        return False, f"Theme is '{theme}', expected 'dark'."

    # Check desktop notifications disabled
    notifications = settings.get("notifications", {})
    desktop = notifications.get("desktop")
    if desktop is not False:
        return False, f"Desktop notifications is {desktop}, expected false."

    # Check sound disabled
    sound = notifications.get("sound")
    if sound is not False:
        return False, f"Notification sound is {sound}, expected false."

    return True, "Dark mode enabled, desktop notifications and sound disabled."
