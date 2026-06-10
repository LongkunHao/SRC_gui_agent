import requests

def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()
    if state["currentUser"]["fullName"] == "Jordan Rivera":
        return True, "Full name successfully changed to 'Jordan Rivera'."
    return False, f"Expected fullName 'Jordan Rivera', got '{state['currentUser']['fullName']}'."
