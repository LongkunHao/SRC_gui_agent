import requests

def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()
    if state["notificationSettings"]["slack"]["enabled"] == True:
        return True, "Slack notification channel correctly enabled."
    return False, f"Expected slack enabled to be True, got {state['notificationSettings']['slack']['enabled']}."
