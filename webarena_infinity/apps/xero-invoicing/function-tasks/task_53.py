import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."

    state = resp.json()
    reminder = next(
        (r for r in state["invoiceReminders"]
         if r["timing"] == "after" and r["days"] == 30),
        None
    )
    if not reminder:
        return False, "Reminder for 30 days after due date not found."

    if reminder["enabled"] is not True:
        return False, f"Reminder enabled is {reminder['enabled']}, expected True."

    return True, "30-day after due date reminder enabled."
