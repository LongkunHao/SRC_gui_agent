# Set home view to Inbox and first day of week to Wednesday
import requests

def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, f"Failed to fetch state: HTTP {resp.status_code}"
    state = resp.json()
    prefs = state.get("preferences", {})
    home = prefs.get("defaultHomeView")
    day = prefs.get("firstDayOfWeek")
    errors = []
    if home != "Inbox":
        errors.append(f"defaultHomeView is '{home}', expected 'Inbox'")
    if day != "Wednesday":
        errors.append(f"firstDayOfWeek is '{day}', expected 'Wednesday'")
    if errors:
        return False, "; ".join(errors)
    return True, "Home view set to Inbox and first day of week set to Wednesday"
