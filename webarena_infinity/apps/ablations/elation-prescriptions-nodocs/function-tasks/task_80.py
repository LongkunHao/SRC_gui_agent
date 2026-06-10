import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."

    state = resp.json()
    settings = state.get("settings", {})

    if settings.get("defaultRefills") != 11:
        return False, f"Default refills should be 11, got {settings.get('defaultRefills')}."

    return True, "Default refills changed to 11."
