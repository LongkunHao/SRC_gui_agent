import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()

    settings = state.get("settings", {})
    errors = []

    # Check auto reminders disabled
    auto_reminders = settings.get("autoReminders", {})
    if auto_reminders.get("enabled") is not False:
        errors.append(f"autoReminders.enabled is {auto_reminders.get('enabled')}, expected false.")

    # Check auto drafts disabled
    auto_drafts = settings.get("autoDrafts", {})
    if auto_drafts.get("enabled") is not False:
        errors.append(f"autoDrafts.enabled is {auto_drafts.get('enabled')}, expected false.")

    # Check Smart Send disabled
    smart_send = settings.get("smartSend", {})
    if smart_send.get("enabled") is not False:
        errors.append(f"smartSend.enabled is {smart_send.get('enabled')}, expected false.")

    if errors:
        return False, " | ".join(errors)

    return True, "Auto reminders, auto drafts, and Smart Send all disabled."
