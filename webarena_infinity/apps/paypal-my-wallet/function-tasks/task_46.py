import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()

    prefs = state.get("walletPreferences", {})
    auto_accept = prefs.get("autoAcceptPayments")

    if auto_accept is not False:
        return False, f"Expected walletPreferences.autoAcceptPayments to be False, got {auto_accept}."

    return True, "Auto-accept payments has been successfully disabled."
