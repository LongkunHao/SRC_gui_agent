# Task: Increase the font size to Large.
import requests

def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, f"Failed to fetch state: HTTP {resp.status_code}"
    state = resp.json()
    size = state.get("preferences", {}).get("fontSize")
    if size == "Large":
        return True, "Font size is set to Large."
    return False, f"Expected fontSize 'Large', got '{size}'."
