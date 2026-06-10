import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()
    try:
        value = state["accountSettings"]["syncSettings"]["googleSyncDeprecationAcknowledged"]
    except KeyError:
        return False, "Could not find accountSettings.syncSettings.googleSyncDeprecationAcknowledged in state."
    if value is False:
        return True, "googleSyncDeprecationAcknowledged is correctly set to False."
    return False, f"Expected googleSyncDeprecationAcknowledged to be False, but got {value}."
