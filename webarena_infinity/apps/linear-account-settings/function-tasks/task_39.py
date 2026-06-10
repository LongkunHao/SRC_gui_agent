import requests

def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()
    if state["notificationSettings"]["mobile"]["cycleUpdated"] == True:
        return True, "Mobile cycle updates notification correctly turned on."
    return False, f"Expected mobile cycleUpdated to be True, got {state['notificationSettings']['mobile']['cycleUpdated']}."
