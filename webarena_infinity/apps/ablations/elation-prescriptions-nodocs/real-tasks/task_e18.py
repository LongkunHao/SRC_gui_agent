import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."

    state = resp.json()

    settings = state.get("settings", {})
    erx_enabled = settings.get("eRxEnabled")

    if erx_enabled is not False:
        return False, f"Expected settings.eRxEnabled to be False, but got {erx_enabled}."

    return True, "Electronic prescribing has been disabled."
