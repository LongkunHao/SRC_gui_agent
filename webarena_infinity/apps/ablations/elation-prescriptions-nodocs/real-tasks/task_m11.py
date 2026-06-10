import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."

    state = resp.json()
    settings = state.get("settings", {})

    if settings.get("printFormat") != "detailed":
        return False, f"Expected settings.printFormat 'detailed', got '{settings.get('printFormat')}'."

    if settings.get("autoCheckInteractions") is not False:
        return False, f"Expected settings.autoCheckInteractions False, got {settings.get('autoCheckInteractions')}."

    return True, "Print format changed to detailed and drug interaction auto-check disabled."
