import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."

    state = resp.json()
    settings = state.get("settings", {})

    if settings.get("defaultDaysSupply") != 7:
        return False, f"Default days supply should be 7, got {settings.get('defaultDaysSupply')}."

    return True, "Default days supply changed to 7."
