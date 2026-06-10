# Task: Display name = capitalized username, home = Current cycle, both auto-assigns on.
import requests

def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, f"Failed to fetch state: HTTP {resp.status_code}"
    state = resp.json()
    failures = []

    # Seed username: "alexmorgan" → capitalize first letter → "Alexmorgan"
    name = state.get("currentUser", {}).get("fullName", "")
    if name != "Alexmorgan":
        failures.append(f"Expected display name 'Alexmorgan', got '{name}'")

    prefs = state.get("preferences", {})
    if prefs.get("defaultHomeView") != "Current cycle":
        failures.append(f"Expected home view 'Current cycle', got '{prefs.get('defaultHomeView')}'")
    if prefs.get("autoAssignOnCreate") is not True:
        failures.append("autoAssignOnCreate should be True")
    if prefs.get("autoAssignOnStarted") is not True:
        failures.append("autoAssignOnStarted should be True")

    if failures:
        return False, "; ".join(failures)
    return True, "Display name set to 'Alexmorgan', home view and auto-assigns configured."
