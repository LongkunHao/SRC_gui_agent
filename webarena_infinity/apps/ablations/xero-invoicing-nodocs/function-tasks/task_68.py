import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()

    inv = next((i for i in state["invoices"] if i["invoiceNumber"] == "INV-0018"), None)
    if not inv:
        return False, "Invoice INV-0018 not found."
    if inv["currency"] != "NZD":
        return False, f"Expected currency 'NZD', got '{inv['currency']}'"
    return True, "Currency of INV-0018 changed from AUD to NZD correctly."
