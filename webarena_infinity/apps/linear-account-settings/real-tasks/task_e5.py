# Task: Turn on auto-assign when creating issues.
import requests

def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, f"Failed to fetch state: HTTP {resp.status_code}"
    state = resp.json()
    val = state.get("preferences", {}).get("autoAssignOnCreate")
    if val is True:
        return True, "autoAssignOnCreate is enabled."
    return False, f"Expected autoAssignOnCreate to be True, got {val}."
