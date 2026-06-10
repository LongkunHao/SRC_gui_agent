import requests

def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()
    if state["notificationSettings"]["mobile"]["enabled"] == False:
        return True, "Mobile notification channel correctly disabled."
    return False, f"Expected mobile enabled to be False, got {state['notificationSettings']['mobile']['enabled']}."
