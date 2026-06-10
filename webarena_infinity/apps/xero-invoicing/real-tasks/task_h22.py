import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."

    state = resp.json()

    inv = next((i for i in state.get("invoices", []) if i.get("number") == "INV-0045"), None)
    if inv is None:
        return False, "Invoice INV-0045 not found."

    # Check payments removed
    if len(inv.get("payments", [])) > 0:
        return False, f"Expected no payments on INV-0045, found {len(inv['payments'])}."

    # Check voided
    if inv.get("status") != "voided":
        return False, f"Expected INV-0045 status 'voided', got '{inv.get('status')}'."

    return True, "INV-0045: partial payment removed and invoice voided."
