import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()

    prefs = state.get("walletPreferences", {})
    instant_transfer = prefs.get("instantTransferPreference")

    if instant_transfer is not False:
        return False, f"Expected walletPreferences.instantTransferPreference to be False, got {instant_transfer}."

    return True, "Instant transfer preference has been successfully disabled."
