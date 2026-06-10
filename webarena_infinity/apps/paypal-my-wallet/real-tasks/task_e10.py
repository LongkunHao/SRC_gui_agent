import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()

    prefs = state.get("walletPreferences")
    if prefs is None:
        return False, "No wallet preferences found in state."

    if prefs.get("instantTransferPreference") is not False:
        return False, f"Instant transfer preference is still enabled (instantTransferPreference={prefs.get('instantTransferPreference')})."

    return True, "Instant transfer preference has been successfully turned off."
