import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()

    enabled = state.get("settings", {}).get("instantReply", {}).get("enabled")
    if enabled is False:
        return True, "Instant Reply is turned off."
    return False, f"Instant Reply is not turned off (enabled={enabled!r})."
