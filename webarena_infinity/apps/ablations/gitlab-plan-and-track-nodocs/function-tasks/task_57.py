import requests

def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."

    state = resp.json()
    subscriptions = state.get("subscriptions", [])
    if 33 not in subscriptions:
        return False, "Issue #33 not found in subscriptions."

    return True, "Subscribed to issue #33."
