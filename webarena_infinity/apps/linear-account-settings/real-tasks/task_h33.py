# Task: Create API key labeled with Acme Corp role, enable both auto-assign settings.
import requests

def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, f"Failed to fetch state: HTTP {resp.status_code}"
    state = resp.json()
    failures = []

    # Role at Acme Corp is 'Admin'
    api_keys = state.get("apiKeys", [])
    labels = [k.get("label") for k in api_keys]
    if "Admin" not in labels:
        failures.append(f"API key labeled 'Admin' not found. Current keys: {labels}")

    prefs = state.get("preferences", {})
    if not prefs.get("autoAssignOnCreate"):
        failures.append("autoAssignOnCreate should be true")
    if not prefs.get("autoAssignOnStarted"):
        failures.append("autoAssignOnStarted should be true")

    if failures:
        return False, "; ".join(failures)
    return True, "API key 'Admin' created and both auto-assign settings enabled."
