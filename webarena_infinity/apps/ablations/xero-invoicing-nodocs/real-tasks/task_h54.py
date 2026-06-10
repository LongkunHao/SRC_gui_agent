"""Verify: Create Kaikoura Marine Research contact + approved USD invoice."""
import requests


def verify(server_url: str) -> tuple[bool, str]:
    state = requests.get(f"{server_url}/api/state", timeout=5).json()
    contacts = state.get("contacts", [])
    invoices = state.get("invoices", [])
    errors = []

    # Check contact
    con = next((c for c in contacts if c["name"] == "Kaikoura Marine Research"), None)
    if not con:
        return False, "Contact 'Kaikoura Marine Research' not found"

    if con.get("email") != "research@kaikouramarine.co.nz":
        errors.append(f"Email is '{con.get('email')}', expected 'research@kaikouramarine.co.nz'")
    phone = (con.get("phone") or "").replace(" ", "")
    if phone != "+6433198000":
        errors.append(f"Phone is '{con.get('phone')}', expected '+64 3 319 8000'")
    addr = con.get("billingAddress", {})
    if addr.get("city") != "Kaikoura":
        errors.append(f"Billing city is '{addr.get('city')}', expected 'Kaikoura'")
    if addr.get("postalCode") != "7300":
        errors.append(f"Postal code is '{addr.get('postalCode')}', expected '7300'")
    if con.get("taxId") != "NZ-62-789-012":
        errors.append(f"Tax ID is '{con.get('taxId')}', expected 'NZ-62-789-012'")

    # Check invoice
    con_invoices = [i for i in invoices if i.get("contactId") == con["id"]]
    if not con_invoices:
        errors.append("No invoice found for Kaikoura Marine Research")
    else:
        inv = con_invoices[0]
        if inv.get("status") != "awaiting_payment":
            errors.append(f"Invoice status is '{inv.get('status')}', expected 'awaiting_payment'")
        if inv.get("currency") != "USD":
            errors.append(f"Currency is '{inv.get('currency')}', expected 'USD'")
        if inv.get("reference") != "MR-2026-001":
            errors.append(f"Reference is '{inv.get('reference')}', expected 'MR-2026-001'")
        if inv.get("issueDate") != "2026-03-18":
            errors.append(f"Issue date is '{inv.get('issueDate')}', expected '2026-03-18'")
        if inv.get("dueDate") != "2026-05-18":
            errors.append(f"Due date is '{inv.get('dueDate')}', expected '2026-05-18'")

        lis = inv.get("lineItems", [])
        if len(lis) < 2:
            errors.append(f"Expected 2 line items, found {len(lis)}")
        else:
            marine = next((l for l in lis if "marine" in (l.get("description") or "").lower()
                           or "survey" in (l.get("description") or "").lower()), None)
            if not marine:
                errors.append("No 'Marine survey' line item found")
            elif abs(marine["quantity"] - 5) > 0.01 or abs(marine["unitPrice"] - 800) > 0.01:
                errors.append(f"Marine line: qty={marine['quantity']} price={marine['unitPrice']}, expected 5 x $800")

            analysis = next((l for l in lis if "analysis" in (l.get("description") or "").lower()
                             or "data" in (l.get("description") or "").lower()
                             or "report" in (l.get("description") or "").lower()), None)
            if not analysis:
                errors.append("No 'Data analysis report' line item found")
            elif abs(analysis["quantity"] - 1) > 0.01 or abs(analysis["unitPrice"] - 3200) > 0.01:
                errors.append(f"Analysis line: qty={analysis['quantity']} price={analysis['unitPrice']}, expected 1 x $3,200")

    if errors:
        return False, "; ".join(errors)
    return True, "Kaikoura Marine Research contact and approved USD invoice created"
