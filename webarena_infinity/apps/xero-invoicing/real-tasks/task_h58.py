import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."

    state = resp.json()
    reminders = state.get("invoiceReminders", [])

    errors = []

    # Check for new 3-day before reminder
    before_3 = [r for r in reminders if r.get("timing") == "before" and r.get("days") == 3 and r.get("enabled")]
    if not before_3:
        errors.append("No enabled reminder found for 3 days before the due date.")

    # All 'after' reminders should be disabled
    after_enabled = [r for r in reminders if r.get("timing") == "after" and r.get("enabled")]
    if after_enabled:
        days_list = [str(r.get("days")) for r in after_enabled]
        errors.append(f"After-due-date reminders still enabled for days: {', '.join(days_list)}.")

    if errors:
        return False, " ".join(errors)

    return True, "3-day pre-due reminder created, all post-due reminders disabled."
