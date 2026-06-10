# Task: Enable the pointer cursor for interactive elements.
import requests

def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, f"Failed to fetch state: HTTP {resp.status_code}"
    state = resp.json()
    val = state.get("preferences", {}).get("usePointerCursor")
    if val is True:
        return True, "Pointer cursor is enabled"
    return False, f"usePointerCursor is {val}, expected True"
