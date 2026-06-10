import requests

def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()
    for app in state["authorizedApps"]:
        if app.get("name") == "Marker.io":
            return False, "Authorized app 'Marker.io' still exists."
    return True, "Authorized app 'Marker.io' successfully revoked."
