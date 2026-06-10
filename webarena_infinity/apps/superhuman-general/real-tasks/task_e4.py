import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()

    theme = state.get("settings", {}).get("theme")
    if theme == "dark":
        return True, "The app is in dark mode."
    return False, f"The app is not in dark mode (theme={theme!r})."
