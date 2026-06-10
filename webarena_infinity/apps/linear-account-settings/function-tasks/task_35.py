import requests

def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()
    if state["notificationSettings"]["email"]["enabled"] == False:
        return True, "Email notification channel correctly disabled."
    return False, f"Expected email enabled to be False, got {state['notificationSettings']['email']['enabled']}."
