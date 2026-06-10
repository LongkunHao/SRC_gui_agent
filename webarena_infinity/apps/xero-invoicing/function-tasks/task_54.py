import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."

    state = resp.json()
    reminder = next(
        (r for r in state["invoiceReminders"]
         if r["timing"] == "after" and r["days"] == 21),
        None
    )
    if not reminder:
        return False, "Reminder for 21 days after due date not found."

    if reminder["enabled"] is not True:
        return False, f"Reminder enabled is {reminder['enabled']}, expected True."

    expected_subject = "Third reminder: Invoice overdue - {InvoiceNumber}"
    if reminder["subject"] != expected_subject:
        return False, f"Reminder subject doesn't match expected value."

    if reminder.get("includeInvoicePdf") is not True:
        return False, "includeInvoicePdf should be True."

    return True, "New reminder created for 21 days after due date."
