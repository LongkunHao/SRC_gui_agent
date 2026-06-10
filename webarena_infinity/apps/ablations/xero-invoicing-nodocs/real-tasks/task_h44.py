"""Verify: Settings prefix/number/padding changed, then new draft for Bloom & Branch."""
import requests


def verify(server_url: str) -> tuple[bool, str]:
    state = requests.get(f"{server_url}/api/state", timeout=5).json()
    invoices = state.get("invoices", [])
    settings = state.get("settings", {})
    errors = []

    # Settings checks
    if settings.get("invoiceNumberPrefix") != "NZ-":
        errors.append(f"prefix is '{settings.get('invoiceNumberPrefix')}', expected 'NZ-'")
    if settings.get("invoiceNumberPadding") != 5:
        errors.append(f"padding is {settings.get('invoiceNumberPadding')}, expected 5")

    # Bloom & Branch Florists = con_15
    con_15_invoices = [i for i in invoices if i.get("contactId") == "con_15" and i.get("status") == "draft"]
    new_drafts = [i for i in con_15_invoices
                  if any("brand" in (li.get("description") or "").lower() for li in i.get("lineItems", []))]
    if not new_drafts:
        errors.append("No new draft invoice with 'brand' line item found for Bloom & Branch Florists (con_15)")
    else:
        inv = new_drafts[0]
        if inv.get("issueDate") != "2026-03-18":
            errors.append(f"Issue date is '{inv.get('issueDate')}', expected '2026-03-18'")
        if inv.get("dueDate") != "2026-04-17":
            errors.append(f"Due date is '{inv.get('dueDate')}', expected '2026-04-17'")
        brand_li = next((l for l in inv.get("lineItems", [])
                         if "brand" in (l.get("description") or "").lower()), None)
        if brand_li:
            if abs(brand_li.get("quantity", 0) - 1) > 0.01:
                errors.append(f"Brand line qty is {brand_li.get('quantity')}, expected 1")
            if abs(brand_li.get("unitPrice", 0) - 3500) > 0.01:
                errors.append(f"Brand line price is {brand_li.get('unitPrice')}, expected 3500")

    if errors:
        return False, "; ".join(errors)
    return True, "Settings updated (NZ- prefix, 5 padding) and new draft invoice created for Bloom & Branch"
