import requests

def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()
    settings = state.get("notificationSettings", {})
    if settings.get("email") is not False:
        return False, f"Email notifications is {settings.get('email')}, expected False."
    return True, "Email notifications disabled."
