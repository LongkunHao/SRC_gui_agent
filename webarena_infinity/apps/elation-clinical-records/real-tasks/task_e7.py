import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()

    prefs = state.get("providerPreferences", {})
    show_dx = prefs.get("showDxCodesInPrint")

    if show_dx is None:
        return False, "Could not find 'showDxCodesInPrint' in providerPreferences."

    if show_dx is not True:
        return False, f"showDxCodesInPrint is {show_dx}, expected True."

    return True, "Successfully verified that 'Show Dx Codes in Print' is turned on."
