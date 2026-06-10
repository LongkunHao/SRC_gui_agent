import requests

def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()
    val = state["preferences"]["fontSize"]
    if val == "Large":
        return True, "Font size successfully changed to 'Large'."
    return False, f"Expected fontSize 'Large', got '{val}'."
