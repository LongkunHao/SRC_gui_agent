import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()

    prefs = state.get("providerPreferences", {})
    show_dx = prefs.get("showDxCodesInPrint")
    if show_dx is True:
        return True, "providerPreferences.showDxCodesInPrint is True."
    return False, f"providerPreferences.showDxCodesInPrint is {show_dx}, expected True."
