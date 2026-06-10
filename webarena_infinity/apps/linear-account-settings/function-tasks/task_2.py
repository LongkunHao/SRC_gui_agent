import requests

def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()
    if state["currentUser"]["username"] == "jrivera":
        return True, "Username successfully changed to 'jrivera'."
    return False, f"Expected username 'jrivera', got '{state['currentUser']['username']}'."
