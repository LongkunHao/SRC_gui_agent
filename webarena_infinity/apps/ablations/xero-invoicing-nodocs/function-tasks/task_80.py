import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()

    inv = next((i for i in state["invoices"] if i["invoiceNumber"] == "INV-0009"), None)
    if not inv:
        return False, "Invoice INV-0009 not found."
    con = next((c for c in state["contacts"] if c["id"] == inv["contactId"]), None)
    if not con:
        return False, "Contact for INV-0009 not found."
    if con["email"] != "accounts@pinnacle.co.nz":
        return False, f"Expected email 'accounts@pinnacle.co.nz', got '{con['email']}'"
    return True, "Email updated for contact associated with INV-0009."
