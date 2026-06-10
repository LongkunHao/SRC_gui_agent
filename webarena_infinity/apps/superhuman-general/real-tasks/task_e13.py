import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()

    swipe_left = state.get("settings", {}).get("swipeLeft")
    if swipe_left == "trash":
        return True, "Swipe left action is set to Trash."
    return False, f"Swipe left action is not set to Trash (swipeLeft={swipe_left!r})."
