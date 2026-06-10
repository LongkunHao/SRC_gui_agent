import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()
    labels = state.get("contactLabels", [])
    for label in labels:
        if label.get("name") == "Conference":
            return True, "Label 'Conference' exists."
    return False, "No label found with name 'Conference'."
