import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."

    state = resp.json()
    reminder = next(
        (r for r in state["invoiceReminders"]
         if r["timing"] == "after" and r["days"] == 14),
        None
    )
    if reminder is not None:
        return False, "Reminder for 14 days after due date still exists."

    return True, "14-day after due date reminder deleted."
