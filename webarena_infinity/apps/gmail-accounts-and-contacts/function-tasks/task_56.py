import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()
    try:
        value = state["accountSettings"]["notificationSettings"]["contactChanges"]
    except KeyError:
        return False, "Could not find accountSettings.notificationSettings.contactChanges in state."
    if value is True:
        return True, "contactChanges is correctly set to True."
    return False, f"Expected contactChanges to be True, but got {value}."
