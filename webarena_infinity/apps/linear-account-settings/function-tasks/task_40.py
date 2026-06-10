import requests

def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()
    if state["notificationSettings"]["email"]["issueCommented"] == True:
        return True, "Email comments on subscribed issues notification correctly turned on."
    return False, f"Expected email issueCommented to be True, got {state['notificationSettings']['email']['issueCommented']}."
