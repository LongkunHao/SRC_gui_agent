# Task: Update the account name to 'Jordan Rivera' and change the username to 'jrivera'.
import requests

def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, f"Failed to fetch state: HTTP {resp.status_code}"
    state = resp.json()
    user = state.get("currentUser", {})
    full_name = user.get("fullName", "")
    username = user.get("username", "")
    errors = []
    if full_name != "Jordan Rivera":
        errors.append(f"Expected fullName 'Jordan Rivera', got '{full_name}'")
    if username != "jrivera":
        errors.append(f"Expected username 'jrivera', got '{username}'")
    if errors:
        return False, "; ".join(errors)
    return True, "Account name and username updated correctly."
