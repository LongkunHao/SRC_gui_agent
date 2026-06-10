import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."

    state = resp.json()

    # Find Greenfield Organics contact
    contact = next((c for c in state.get("contacts", []) if "Greenfield" in c.get("name", "")), None)
    if contact is None:
        return False, "Greenfield Organics contact not found."
    gf_id = contact.get("id")

    # Find Greenfield invoice with e-commerce line item
    invoices = state.get("invoices", [])
    gf_invoices = [inv for inv in invoices if inv.get("contactId") == gf_id]

    ecom_invoice = None
    for inv in gf_invoices:
        for li in inv.get("lineItems", []):
            desc = li.get("description", "").lower()
            if "e-commerce" in desc or "ecommerce" in desc:
                ecom_invoice = inv
                break
        if ecom_invoice:
            break

    if ecom_invoice is None:
        return False, "No Greenfield Organics invoice with e-commerce line item found."

    if ecom_invoice.get("reference") != "GF-ECOM-2026":
        return False, f"Expected reference 'GF-ECOM-2026', got '{ecom_invoice.get('reference')}'."

    return True, f"{ecom_invoice.get('number')} reference updated to 'GF-ECOM-2026'."
