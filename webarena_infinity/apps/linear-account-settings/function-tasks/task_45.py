import requests

def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()
    if state["notificationSettings"]["receiveDpaUpdates"] == False:
        return True, "'DPA updates' communication successfully turned off."
    return False, f"Expected receiveDpaUpdates to be False, got {state['notificationSettings']['receiveDpaUpdates']}."
