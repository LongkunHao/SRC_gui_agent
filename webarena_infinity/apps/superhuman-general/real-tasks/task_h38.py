import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()

    settings = state.get("settings", {})
    errors = []

    # 1. Read receipt team sharing disabled
    team_sharing = settings.get("readReceipts", {}).get("teamSharing")
    if team_sharing is not False:
        errors.append(f"Read receipt team sharing is {team_sharing}, expected false.")

    # 2. Auto reminders set to manual mode
    auto_mode = settings.get("autoReminders", {}).get("mode")
    if auto_mode != "manual":
        errors.append(f"Auto reminders mode is '{auto_mode}', expected 'manual'.")

    # 3. Calendar alerts set to 5 minutes
    alert_minutes = settings.get("notifications", {}).get("alertMinutes")
    if alert_minutes != 5:
        errors.append(f"Calendar alert minutes is {alert_minutes}, expected 5.")

    if errors:
        return False, " ".join(errors)

    return True, "Read receipt team sharing disabled, auto reminders set to manual, calendar alerts set to 5 minutes."
