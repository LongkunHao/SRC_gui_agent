import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."

    state = resp.json()

    # Find TechVault contact
    contact = next((c for c in state.get("contacts", []) if "TechVault" in c.get("name", "")), None)
    if contact is None:
        return False, "TechVault Solutions contact not found."
    tv_id = contact.get("id")

    # Find TechVault invoices with security audit line item
    invoices = state.get("invoices", [])
    tv_invoices = [inv for inv in invoices if inv.get("contactId") == tv_id]

    audit_invoice = None
    for inv in tv_invoices:
        for li in inv.get("lineItems", []):
            desc = li.get("description", "").lower()
            if "security audit" in desc:
                audit_invoice = inv
                break
        if audit_invoice:
            break

    if audit_invoice is None:
        return False, "No TechVault invoice with a security audit line item found."

    if audit_invoice.get("status") != "voided":
        return False, f"Expected {audit_invoice.get('number')} status 'voided', got '{audit_invoice.get('status')}'."

    return True, f"{audit_invoice.get('number')} (TechVault, security audit) voided."
