import requests

def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()
    for app in state["authorizedApps"]:
        if app.get("name") == "Zapier":
            return False, "Authorized app 'Zapier' still exists."
    return True, "Authorized app 'Zapier' successfully revoked."
