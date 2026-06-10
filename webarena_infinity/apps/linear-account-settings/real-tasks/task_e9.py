# Task: Revoke the Zapier integration.
import requests

def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, f"Failed to fetch state: HTTP {resp.status_code}"
    state = resp.json()
    apps = state.get("authorizedApps", [])
    for app in apps:
        if app.get("name") == "Zapier":
            return False, "Zapier authorized app still exists."
    return True, "Zapier integration has been revoked."
