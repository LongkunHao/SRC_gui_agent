# Task: Revoke all authorized third-party applications.
import requests

def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, f"Failed to fetch state: HTTP {resp.status_code}"
    state = resp.json()
    apps = state.get("authorizedApps", [])

    if len(apps) != 0:
        names = [a.get("name", "unknown") for a in apps]
        return False, f"Expected 0 authorized apps, found {len(apps)}: {names}"
    return True, "All authorized apps revoked."
