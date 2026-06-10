import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."

    state = resp.json()
    invoices = state.get("invoices", [])

    # Find Alpha Logistics contact
    contact = next((c for c in state.get("contacts", []) if "Alpha Logistics" in c.get("name", "")), None)
    if contact is None:
        return False, "Alpha Logistics contact not found."
    alpha_id = contact.get("id")

    # Find new draft invoice for Alpha Logistics with total ~$13,255 (same as INV-0050)
    # and reference ALI-2026-Q2
    new_inv = next(
        (inv for inv in invoices
         if inv.get("contactId") == alpha_id
         and inv.get("status") == "draft"
         and abs(inv.get("total", 0) - 13255.00) < 5.00
         and inv.get("number") != "INV-0050"),
        None
    )
    if new_inv is None:
        return False, "No new draft invoice found for Alpha Logistics with total ~$13,255."

    if new_inv.get("reference") != "ALI-2026-Q2":
        return False, f"Expected reference 'ALI-2026-Q2', got '{new_inv.get('reference')}'."

    return True, f"Invoice {new_inv.get('number')} copied from INV-0050 with reference 'ALI-2026-Q2'."
