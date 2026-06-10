import requests

def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()
    if state["currentUser"]["avatarColor"] != "#5E6AD2":
        return True, f"Avatar color changed from seed value to '{state['currentUser']['avatarColor']}'."
    return False, "Avatar color is still the seed value '#5E6AD2'."
