"""Verify: Bold Corporate theme + AU GST default, new AUD invoice for Australian contact approved and sent."""
import requests


def verify(server_url: str) -> tuple[bool, str]:
    state = requests.get(f"{server_url}/api/state", timeout=5).json()
    invoices = state.get("invoices", [])
    settings = state.get("settings", {})
    errors = []

    # Settings
    if settings.get("defaultBrandingThemeId") != "theme_4":
        errors.append(f"defaultBrandingThemeId is '{settings.get('defaultBrandingThemeId')}', expected 'theme_4' (Bold Corporate)")
    if settings.get("defaultTaxRateId") != "tax_7":
        errors.append(f"defaultTaxRateId is '{settings.get('defaultTaxRateId')}', expected 'tax_7' (AU GST)")

    # New AUD invoice for CloudBridge Software (con_21), approved and sent
    # Seed invoices for CloudBridge: inv_46 (paid), inv_71 (paid), inv_96 (paid) — no AP in seed
    new_ap = [i for i in invoices
              if i.get("contactId") == "con_21"
              and i.get("status") == "awaiting_payment"
              and i.get("sentAt")]
    if not new_ap:
        # Try just awaiting_payment without sentAt check
        new_ap_nosent = [i for i in invoices
                         if i.get("contactId") == "con_21"
                         and i.get("status") == "awaiting_payment"]
        if new_ap_nosent:
            errors.append("Invoice for CloudBridge found but not sent (sentAt is null)")
        else:
            errors.append("No approved invoice found for CloudBridge Software (con_21)")
    else:
        inv = new_ap[0]
        if inv.get("currency") != "AUD":
            errors.append(f"Invoice currency is '{inv.get('currency')}', expected 'AUD'")
        if inv.get("issueDate") != "2026-03-18":
            errors.append(f"Issue date is '{inv.get('issueDate')}', expected '2026-03-18'")
        if inv.get("dueDate") != "2026-06-18":
            errors.append(f"Due date is '{inv.get('dueDate')}', expected '2026-06-18'")
        if inv.get("reference") != "AU-SUPPORT-2026":
            errors.append(f"Reference is '{inv.get('reference')}', expected 'AU-SUPPORT-2026'")
        lis = inv.get("lineItems", [])
        if len(lis) < 2:
            errors.append(f"Expected 2 line items, found {len(lis)}")
        else:
            support = next((l for l in lis if "support" in (l.get("description") or "").lower()
                            or "annual" in (l.get("description") or "").lower()), None)
            if not support:
                errors.append("No 'Annual support contract' line item found")
            elif abs(support["quantity"] - 1) > 0.01 or abs(support["unitPrice"] - 12000) > 0.01:
                errors.append(f"Support line: qty={support['quantity']} price={support['unitPrice']}, expected 1 x $12,000")
            impl = next((l for l in lis if "implementation" in (l.get("description") or "").lower()
                         or "fee" in (l.get("description") or "").lower()), None)
            if not impl:
                errors.append("No 'Implementation fee' line item found")
            elif abs(impl["quantity"] - 1) > 0.01 or abs(impl["unitPrice"] - 5000) > 0.01:
                errors.append(f"Impl line: qty={impl['quantity']} price={impl['unitPrice']}, expected 1 x $5,000")

    if errors:
        return False, "; ".join(errors)
    return True, "Settings updated; AUD invoice for CloudBridge created, approved, and sent"
