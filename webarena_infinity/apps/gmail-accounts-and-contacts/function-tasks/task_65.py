import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()
    try:
        phone = state["currentUser"]["phone"]
    except KeyError:
        return False, "Could not find currentUser.phone in state."
    if phone == "+1 (650) 555-7777":
        return True, "currentUser.phone is correctly set to '+1 (650) 555-7777'."
    return False, f"Expected currentUser.phone to be '+1 (650) 555-7777', but got '{phone}'."
