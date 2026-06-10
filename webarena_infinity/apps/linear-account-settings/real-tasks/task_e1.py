# Task: Switch the interface to dark mode.
import requests

def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, f"Failed to fetch state: HTTP {resp.status_code}"
    state = resp.json()
    theme = state.get("preferences", {}).get("interfaceTheme")
    if theme == "Dark":
        return True, "Interface theme is set to Dark."
    return False, f"Expected interfaceTheme 'Dark', got '{theme}'."
