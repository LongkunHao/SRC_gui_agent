import requests

def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()
    val = state["preferences"]["interfaceTheme"]
    if val == "Light - Contrast":
        return True, "Interface theme successfully changed to 'Light - Contrast'."
    return False, f"Expected interfaceTheme 'Light - Contrast', got '{val}'."
