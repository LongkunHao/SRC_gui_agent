import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()

    # Check calendar alert timing is set to 15 minutes
    settings = state.get("settings", {})
    notifications = settings.get("notifications", {})
    alert_minutes = notifications.get("alertMinutes")

    if alert_minutes == 15:
        return True, "Calendar alert timing has been successfully changed to 15 minutes."
    else:
        return False, f"Calendar alert timing is {alert_minutes} minutes, expected 15."
