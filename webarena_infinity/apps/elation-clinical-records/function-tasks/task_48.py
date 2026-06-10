import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()

    prefs = state.get("providerPreferences", {})
    coded = prefs.get("codedAssessments")
    if coded is False:
        return True, "providerPreferences.codedAssessments is False."
    return False, f"providerPreferences.codedAssessments is {coded}, expected False."
