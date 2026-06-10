"""Verify: Default tax rate to Zero Rated, create draft invoice for Ironclad Security."""
import requests


def verify(server_url: str) -> tuple[bool, str]:
    state = requests.get(f"{server_url}/api/state", timeout=5).json()
    invoices = state.get("invoices", [])
    settings = state.get("settings", {})
    errors = []

    # Settings check
    if settings.get("defaultTaxRateId") != "tax_5":
        errors.append(f"defaultTaxRateId is '{settings.get('defaultTaxRateId')}', expected 'tax_5' (Zero Rated)")

    # New draft invoice for Ironclad Security Systems (con_16)
    con_16_invoices = [i for i in invoices if i.get("contactId") == "con_16" and i.get("status") == "draft"]
    # Filter to new invoices (seed has no drafts for con_16)
    if not con_16_invoices:
        errors.append("No draft invoice found for Ironclad Security Systems (con_16)")
    else:
        inv = con_16_invoices[0]
        if inv.get("issueDate") != "2026-03-18":
            errors.append(f"Issue date is '{inv.get('issueDate')}', expected '2026-03-18'")
        if inv.get("dueDate") != "2026-03-25":
            errors.append(f"Due date is '{inv.get('dueDate')}', expected '2026-03-25'")
        if inv.get("reference") != "EMRG-001":
            errors.append(f"Reference is '{inv.get('reference')}', expected 'EMRG-001'")

        lis = inv.get("lineItems", [])
        if len(lis) < 2:
            errors.append(f"Expected 2 line items, found {len(lis)}")
        else:
            callout = next((l for l in lis if "emergency" in (l.get("description") or "").lower()
                            or "callout" in (l.get("description") or "").lower()), None)
            if not callout:
                errors.append("No 'Emergency callout' line item found")
            elif abs(callout["quantity"] - 1) > 0.01 or abs(callout["unitPrice"] - 750) > 0.01:
                errors.append(f"Callout line: qty={callout['quantity']} price={callout['unitPrice']}, expected 1 x $750")

            parts = next((l for l in lis if "parts" in (l.get("description") or "").lower()
                          or "replacement" in (l.get("description") or "").lower()), None)
            if not parts:
                errors.append("No 'Replacement parts' line item found")
            elif abs(parts["quantity"] - 4) > 0.01 or abs(parts["unitPrice"] - 125) > 0.01:
                errors.append(f"Parts line: qty={parts['quantity']} price={parts['unitPrice']}, expected 4 x $125")

    if errors:
        return False, "; ".join(errors)
    return True, "Default tax rate set to Zero Rated; draft invoice created for Ironclad Security"
