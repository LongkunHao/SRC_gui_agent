import requests

def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()
    if state["notificationSettings"]["desktop"]["enabled"] == False:
        return True, "Desktop notification channel correctly disabled."
    return False, f"Expected desktop enabled to be False, got {state['notificationSettings']['desktop']['enabled']}."
