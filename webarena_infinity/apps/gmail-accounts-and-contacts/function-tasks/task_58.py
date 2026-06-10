import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()
    try:
        value = state["accountSettings"]["notificationSettings"]["linkedServiceUpdates"]
    except KeyError:
        return False, "Could not find accountSettings.notificationSettings.linkedServiceUpdates in state."
    if value is False:
        return True, "linkedServiceUpdates is correctly set to False."
    return False, f"Expected linkedServiceUpdates to be False, but got {value}."
