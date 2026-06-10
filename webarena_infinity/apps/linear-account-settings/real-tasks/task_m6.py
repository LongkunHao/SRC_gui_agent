# Task: Turn off email notifications for status changes but turn on notifications for comments.
import requests

def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, f"Failed to fetch state: HTTP {resp.status_code}"
    state = resp.json()
    email_notifs = state.get("notificationSettings", {}).get("email", {})
    status_changed = email_notifs.get("issueStatusChanged")
    commented = email_notifs.get("issueCommented")
    errors = []
    if status_changed is not False:
        errors.append(f"Expected issueStatusChanged == False, got {status_changed}")
    if commented is not True:
        errors.append(f"Expected issueCommented == True, got {commented}")
    if errors:
        return False, "; ".join(errors)
    return True, "Email notification settings updated correctly."
