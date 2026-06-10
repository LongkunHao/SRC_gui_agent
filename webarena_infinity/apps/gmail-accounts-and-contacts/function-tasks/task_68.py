import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()
    try:
        value = state["accountSettings"]["privacySettings"]["showProfilePhoto"]
    except KeyError:
        return False, "Could not find accountSettings.privacySettings.showProfilePhoto in state."
    if value == "nobody":
        return True, "showProfilePhoto is correctly set to 'nobody'."
    return False, f"Expected showProfilePhoto to be 'nobody', but got '{value}'."
