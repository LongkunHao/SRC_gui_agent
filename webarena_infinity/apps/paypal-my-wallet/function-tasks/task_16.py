import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()

    balances = state.get("balances", [])
    for b in balances:
        if b.get("currency") == "CAD":
            return False, "CAD currency still exists in balances array. It should have been removed."

    return True, "CAD currency was successfully removed from balances."
