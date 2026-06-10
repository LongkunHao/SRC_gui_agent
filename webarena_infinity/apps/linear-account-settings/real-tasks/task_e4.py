# Task: Change the username to 'amorgan'.
import requests

def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, f"Failed to fetch state: HTTP {resp.status_code}"
    state = resp.json()
    username = state.get("currentUser", {}).get("username")
    if username == "amorgan":
        return True, "Username is 'amorgan'."
    return False, f"Expected username 'amorgan', got '{username}'."
