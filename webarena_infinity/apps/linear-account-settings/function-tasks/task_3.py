import requests

def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()
    if state["currentUser"]["email"] == "jordan.rivera@newcorp.io":
        return True, "Email successfully changed to 'jordan.rivera@newcorp.io'."
    return False, f"Expected email 'jordan.rivera@newcorp.io', got '{state['currentUser']['email']}'."
