import requests

def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()
    val = state["preferences"]["fontSize"]
    if val == "Small":
        return True, "Font size successfully changed to 'Small'."
    return False, f"Expected fontSize 'Small', got '{val}'."
