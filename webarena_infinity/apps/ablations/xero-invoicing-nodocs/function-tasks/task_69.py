import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()

    inv = next((i for i in state["invoices"] if i["invoiceNumber"] == "INV-0025"), None)
    if not inv:
        return False, "Invoice INV-0025 not found."
    if inv["issueDate"] != "2026-03-01":
        return False, f"Expected issue date '2026-03-01', got '{inv['issueDate']}'"
    return True, "Issue date of INV-0025 changed to 2026-03-01 correctly."
