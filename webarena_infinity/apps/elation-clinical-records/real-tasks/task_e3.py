import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()

    prefs = state.get("providerPreferences", {})
    coded = prefs.get("codedAssessments")

    if coded is None:
        return False, "Could not find 'codedAssessments' in providerPreferences."

    if coded is not False:
        return False, f"codedAssessments is {coded}, expected False."

    return True, "Successfully verified that coded visit note assessments are turned off."
