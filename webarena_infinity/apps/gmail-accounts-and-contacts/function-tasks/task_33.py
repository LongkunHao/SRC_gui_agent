import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()

    delegates = state.get("delegates", [])
    for delegate in delegates:
        if delegate.get("email") == "priya.sharma@cloudnine.dev":
            return False, "Delegate with email 'priya.sharma@cloudnine.dev' still exists."

    return True, "No delegate with email 'priya.sharma@cloudnine.dev' exists."
