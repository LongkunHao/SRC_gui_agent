import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."

    state = resp.json()
    reminder = next(
        (r for r in state["invoiceReminders"]
         if r["timing"] == "after" and r["days"] == 1),
        None
    )
    if not reminder:
        return False, "Reminder for 1 day after due date not found."

    expected_subject = "Payment Required - {InvoiceNumber}"
    if reminder["subject"] != expected_subject:
        return False, f"Reminder subject is '{reminder['subject']}', expected '{expected_subject}'."

    return True, "1-day after due date reminder subject updated."
