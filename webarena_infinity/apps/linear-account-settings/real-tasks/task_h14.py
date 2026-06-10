# Task: Turn on auto-assign for both issue creation and moving to started,
# and switch home view to Current cycle.
import requests

def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, f"Failed to fetch state: HTTP {resp.status_code}"
    state = resp.json()
    prefs = state.get("preferences", {})

    checks = [
        (prefs.get("autoAssignOnCreate") == True, f"autoAssignOnCreate: expected True, got {prefs.get('autoAssignOnCreate')}"),
        (prefs.get("autoAssignOnStarted") == True, f"autoAssignOnStarted: expected True, got {prefs.get('autoAssignOnStarted')}"),
        (prefs.get("defaultHomeView") == "Current cycle", f"defaultHomeView: expected 'Current cycle', got '{prefs.get('defaultHomeView')}'"),
    ]

    failures = [msg for ok, msg in checks if not ok]
    if failures:
        return False, "; ".join(failures)
    return True, "Auto-assign settings enabled and home view set to Current cycle."
