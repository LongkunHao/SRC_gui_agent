import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()

    # Check auto reminders mode is set to "external"
    settings = state.get("settings", {})
    auto_reminders = settings.get("autoReminders", {})
    mode = auto_reminders.get("mode")

    if mode == "external":
        return True, "Auto reminders mode has been successfully changed to 'All external' (external)."
    else:
        return False, f"Auto reminders mode is '{mode}', expected 'external'."
