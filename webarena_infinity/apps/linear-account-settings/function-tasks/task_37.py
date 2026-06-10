import requests

def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()
    if state["notificationSettings"]["desktop"]["issueAssigned"] == False:
        return True, "Desktop issue assigned notification correctly turned off."
    return False, f"Expected desktop issueAssigned to be False, got {state['notificationSettings']['desktop']['issueAssigned']}."
