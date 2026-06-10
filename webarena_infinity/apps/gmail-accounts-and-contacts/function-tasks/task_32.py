import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()

    delegates = state.get("delegates", [])
    for delegate in delegates:
        if delegate.get("email") == "jake.morrison@gmail.com":
            return False, "Delegate with email 'jake.morrison@gmail.com' still exists."

    return True, "No delegate with email 'jake.morrison@gmail.com' exists."
