import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."

    state = resp.json()
    settings = state.get("invoiceSettings", {})

    # Check default due date: 7 days after end of invoice month
    due_date = settings.get("defaultDueDate", {})
    if due_date.get("type") != "daysAfterEndOfMonth":
        return False, f"Expected due date type 'daysAfterEndOfMonth', got '{due_date.get('type')}'."
    if due_date.get("days") != 7:
        return False, f"Expected due date days=7, got {due_date.get('days')}."

    # Check credit note prefix
    if settings.get("creditNotePrefix") != "CREDIT-":
        return False, f"Expected credit note prefix 'CREDIT-', got '{settings.get('creditNotePrefix')}'."

    return True, "Default due date set to 7 days after end of month; credit note prefix changed to 'CREDIT-'."
