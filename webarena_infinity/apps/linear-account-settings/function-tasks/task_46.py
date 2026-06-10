import requests

def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()
    if state["notificationSettings"]["receiveProductUpdates"] == True:
        return True, "'Product updates' communication successfully turned on."
    return False, f"Expected receiveProductUpdates to be True, got {state['notificationSettings']['receiveProductUpdates']}."
