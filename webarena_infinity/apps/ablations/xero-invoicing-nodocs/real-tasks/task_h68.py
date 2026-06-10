"""Verify: Late penalties 2% weekly, Minimal Clean theme, new contact + approved invoice."""
import requests


def verify(server_url: str) -> tuple[bool, str]:
    state = requests.get(f"{server_url}/api/state", timeout=5).json()
    invoices = state.get("invoices", [])
    contacts = state.get("contacts", [])
    settings = state.get("settings", {})
    errors = []

    # Settings
    if not settings.get("latePenaltyEnabled"):
        errors.append("latePenaltyEnabled is False, expected True")
    if abs(settings.get("latePenaltyRate", 0) - 2) > 0.01:
        errors.append(f"latePenaltyRate is {settings.get('latePenaltyRate')}, expected 2")
    if settings.get("latePenaltyFrequency") != "weekly":
        errors.append(f"latePenaltyFrequency is '{settings.get('latePenaltyFrequency')}', expected 'weekly'")
    if settings.get("defaultBrandingThemeId") != "theme_3":
        errors.append(f"defaultBrandingThemeId is '{settings.get('defaultBrandingThemeId')}', expected 'theme_3' (Minimal Clean)")

    # New contact
    con = next((c for c in contacts if c["name"] == "Peninsula Consulting Group"), None)
    if not con:
        errors.append("Contact 'Peninsula Consulting Group' not found")
    else:
        if con.get("email") != "billing@peninsula.co.nz":
            errors.append(f"Contact email is '{con.get('email')}', expected 'billing@peninsula.co.nz'")
        if con.get("phone") != "+64 9 445 2200":
            errors.append(f"Contact phone is '{con.get('phone')}', expected '+64 9 445 2200'")
        addr = con.get("billingAddress", {})
        if addr.get("city") != "Takapuna":
            errors.append(f"Contact city is '{addr.get('city')}', expected 'Takapuna'")
        if addr.get("postalCode") != "0622":
            errors.append(f"Contact postalCode is '{addr.get('postalCode')}', expected '0622'")

        # Approved invoice for this contact
        con_invoices = [i for i in invoices if i.get("contactId") == con["id"]
                        and i.get("status") == "awaiting_payment"]
        if not con_invoices:
            errors.append("No approved invoice found for Peninsula Consulting Group")
        else:
            inv = con_invoices[0]
            if inv.get("issueDate") != "2026-03-18":
                errors.append(f"Invoice issueDate is '{inv.get('issueDate')}', expected '2026-03-18'")
            if inv.get("dueDate") != "2026-04-17":
                errors.append(f"Invoice dueDate is '{inv.get('dueDate')}', expected '2026-04-17'")
            if inv.get("reference") != "PEN-001":
                errors.append(f"Invoice reference is '{inv.get('reference')}', expected 'PEN-001'")
            lis = inv.get("lineItems", [])
            if len(lis) < 2:
                errors.append(f"Expected 2 line items, found {len(lis)}")
            else:
                workshop = next((l for l in lis if "planning" in (l.get("description") or "").lower()
                                 or "workshop" in (l.get("description") or "").lower()), None)
                if not workshop:
                    errors.append("No 'Strategic planning workshop' line item found")
                elif abs(workshop["quantity"] - 2) > 0.01 or abs(workshop["unitPrice"] - 1500) > 0.01:
                    errors.append(f"Workshop line: qty={workshop['quantity']} price={workshop['unitPrice']}, expected 2 x $1,500")
                review = next((l for l in lis if "review" in (l.get("description") or "").lower()
                               or "follow" in (l.get("description") or "").lower()), None)
                if not review:
                    errors.append("No 'Follow-up review session' line item found")
                elif abs(review["quantity"] - 1) > 0.01 or abs(review["unitPrice"] - 800) > 0.01:
                    errors.append(f"Review line: qty={review['quantity']} price={review['unitPrice']}, expected 1 x $800")

    if errors:
        return False, "; ".join(errors)
    return True, "Settings updated, Peninsula Consulting Group created with approved invoice"
