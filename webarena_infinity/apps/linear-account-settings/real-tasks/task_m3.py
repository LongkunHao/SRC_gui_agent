# Task: Change the email to 'alex.morgan@newcompany.com'.
import requests

def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, f"Failed to fetch state: HTTP {resp.status_code}"
    state = resp.json()
    email = state.get("currentUser", {}).get("email", "")
    if email != "alex.morgan@newcompany.com":
        return False, f"Expected email 'alex.morgan@newcompany.com', got '{email}'"
    return True, "Email updated correctly."
