import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()
    try:
        value = state["accountSettings"]["privacySettings"]["showPhone"]
    except KeyError:
        return False, "Could not find accountSettings.privacySettings.showPhone in state."
    if value == "everyone":
        return True, "showPhone is correctly set to 'everyone'."
    return False, f"Expected showPhone to be 'everyone', but got '{value}'."
