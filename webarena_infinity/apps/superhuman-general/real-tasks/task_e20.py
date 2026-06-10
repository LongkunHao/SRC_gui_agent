import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()

    calendar_alerts = state.get("settings", {}).get("notifications", {}).get("calendarAlerts")
    if calendar_alerts is False:
        return True, "Calendar alerts are disabled."
    return False, f"Calendar alerts are not disabled (calendarAlerts={calendar_alerts!r})."
