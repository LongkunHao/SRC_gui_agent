import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."

    state = resp.json()
    settings = state.get("settings", {})

    if settings.get("defaultRefills") != 5:
        return False, f"Default refills should be 5, got {settings.get('defaultRefills')}."

    if settings.get("signatureRequired") is not False:
        return False, f"signatureRequired should be False, got {settings.get('signatureRequired')}."

    return True, "Default refills changed to 5 and signature requirement disabled."
