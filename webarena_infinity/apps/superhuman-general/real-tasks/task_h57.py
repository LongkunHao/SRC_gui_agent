import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()

    settings = state.get("settings", {})
    errors = []

    # Ask AI disabled
    ask_ai = settings.get("askAi", {})
    if ask_ai.get("enabled") is not False:
        errors.append(f"Ask AI is still enabled (expected disabled).")

    # Auto-add meeting links disabled
    meeting_link = settings.get("meetingLink", {})
    if meeting_link.get("autoAdd") is not False:
        errors.append(f"Auto-add meeting links is still enabled (expected disabled).")

    # Auto reminders in manual mode
    auto_reminders = settings.get("autoReminders", {})
    if auto_reminders.get("mode") != "manual":
        errors.append(f"Auto reminders mode is '{auto_reminders.get('mode')}', expected 'manual'.")

    # Swipe left changed to Remind
    swipe_left = settings.get("swipeLeft", "")
    if swipe_left != "remind":
        errors.append(f"Swipe left action is '{swipe_left}', expected 'remind'.")

    if errors:
        return False, " ".join(errors)

    return True, "Ask AI disabled, auto-add meeting links off, auto reminders manual, swipe left set to remind."
