import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()

    prefs = state.get("walletPreferences")
    if prefs is None:
        return False, "No wallet preferences found in state."

    if prefs.get("autoAcceptPayments") is not False:
        return False, f"Auto-accept payments is still enabled (autoAcceptPayments={prefs.get('autoAcceptPayments')})."

    return True, "Auto-accept payments has been successfully turned off."
