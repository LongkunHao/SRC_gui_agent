import requests

def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()
    if state["preferences"]["autoAssignOnCreate"] == True:
        return True, "Auto-assign on create toggle correctly turned on."
    return False, f"Expected autoAssignOnCreate to be True, got {state['preferences']['autoAssignOnCreate']}."
