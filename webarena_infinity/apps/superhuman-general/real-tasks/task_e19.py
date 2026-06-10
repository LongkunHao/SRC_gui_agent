import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()

    auto_add = state.get("settings", {}).get("meetingLink", {}).get("autoAdd")
    if auto_add is False:
        return True, "Auto-add meeting links is turned off."
    return False, f"Auto-add meeting links is not turned off (autoAdd={auto_add!r})."
