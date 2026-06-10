import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()

    prefs = state.get("providerPreferences", {})
    fmt = prefs.get("defaultNoteFormat")

    if fmt is None:
        return False, "Could not find 'defaultNoteFormat' in providerPreferences."

    if fmt != "simple":
        return False, f"defaultNoteFormat is '{fmt}', expected 'simple'."

    return True, "Successfully verified that the default note format is set to 'simple'."
