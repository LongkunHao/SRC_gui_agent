import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()
    current_user = state.get("currentUser", {})
    name = current_user.get("name")
    if name == "Alexander Johnson":
        return True, "currentUser.name is 'Alexander Johnson'."
    return False, f"currentUser.name is '{name}', expected 'Alexander Johnson'."
