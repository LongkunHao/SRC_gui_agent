import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."

    state = resp.json()
    settings = state.get("invoiceSettings", {})
    due_date = settings.get("defaultDueDate", {})

    if due_date.get("type") != "endOfFollowingMonth":
        return False, f"Default due date type is '{due_date.get('type')}', expected 'endOfFollowingMonth'."

    return True, "Default due date changed to 'of the following month'."
