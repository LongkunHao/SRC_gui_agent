import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()

    settings = state.get("settings", {})
    expected = "Dear {ContactName},\n\nPlease find invoice {InvoiceNumber} for {Total} attached.\n\nDue: {DueDate}\n\nKiwi Consulting Ltd"
    actual = settings.get("defaultEmailBody", "")
    if actual != expected:
        return False, f"Expected email body template to be updated. Got: {actual!r}"
    return True, "Default email body template updated correctly."
