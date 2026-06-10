# Revoke access for the Notion Integration and Linear Exporter authorized apps
import requests

def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, f"Failed to fetch state: HTTP {resp.status_code}"
    state = resp.json()
    apps = state.get("authorizedApps", [])
    names = [a.get("name") for a in apps]
    if "Notion Integration" in names:
        return False, "Notion Integration is still in authorizedApps"
    if "Linear Exporter" in names:
        return False, "Linear Exporter is still in authorizedApps"
    return True, "Both Notion Integration and Linear Exporter have been revoked"
