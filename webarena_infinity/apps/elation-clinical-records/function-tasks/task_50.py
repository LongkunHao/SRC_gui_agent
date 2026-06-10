import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()

    prefs = state.get("providerPreferences", {})
    fmt = prefs.get("defaultNoteFormat")
    if fmt == "simple":
        return True, "providerPreferences.defaultNoteFormat is 'simple'."
    return False, f"providerPreferences.defaultNoteFormat is '{fmt}', expected 'simple'."
