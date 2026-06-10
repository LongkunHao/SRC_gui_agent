import requests


def verify(server_url: str) -> tuple[bool, str]:
    """Verify reminder rem_10 (James Rodriguez appointment) is acknowledged."""
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, f"Failed to fetch state: HTTP {resp.status_code}"

    state = resp.json()
    reminders = state.get("reminders", [])

    reminder = None
    for r in reminders:
        if r.get("id") == "rem_10":
            reminder = r
            break

    if reminder is None:
        return False, "Reminder rem_10 not found in reminders"

    if reminder.get("acknowledged") is not True:
        return False, f"Reminder rem_10 acknowledged is {reminder.get('acknowledged')}, expected True"

    return True, "Reminder rem_10 (James Rodriguez appointment reminder) acknowledged successfully"
