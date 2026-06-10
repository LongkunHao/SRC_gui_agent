"""Verify: New contact Wairau Valley Vineyards created, AUD invoice with 3 line items approved."""
import requests


def verify(server_url: str) -> tuple[bool, str]:
    state = requests.get(f"{server_url}/api/state", timeout=5).json()
    invoices = state.get("invoices", [])
    contacts = state.get("contacts", [])
    errors = []

    # New contact
    con = next((c for c in contacts if c["name"] == "Wairau Valley Vineyards"), None)
    if not con:
        errors.append("Contact 'Wairau Valley Vineyards' not found")
    else:
        if con.get("email") != "wine@wairauvalley.co.nz":
            errors.append(f"Email is '{con.get('email')}', expected 'wine@wairauvalley.co.nz'")
        if con.get("phone") != "+64 3 572 8800":
            errors.append(f"Phone is '{con.get('phone')}', expected '+64 3 572 8800'")
        addr = con.get("billingAddress", {})
        if addr.get("city") != "Blenheim":
            errors.append(f"City is '{addr.get('city')}', expected 'Blenheim'")
        if addr.get("region") != "Marlborough":
            errors.append(f"Region is '{addr.get('region')}', expected 'Marlborough'")
        if addr.get("postalCode") != "7273":
            errors.append(f"PostalCode is '{addr.get('postalCode')}', expected '7273'")
        if con.get("taxId") != "NZ-71-234-567":
            errors.append(f"TaxId is '{con.get('taxId')}', expected 'NZ-71-234-567'")

        # Approved AUD invoice for this contact
        con_invoices = [i for i in invoices if i.get("contactId") == con["id"]
                        and i.get("status") == "awaiting_payment"]
        if not con_invoices:
            errors.append("No approved invoice found for Wairau Valley Vineyards")
        else:
            inv = con_invoices[0]
            if inv.get("currency") != "AUD":
                errors.append(f"Invoice currency is '{inv.get('currency')}', expected 'AUD'")
            if inv.get("issueDate") != "2026-03-18":
                errors.append(f"Issue date is '{inv.get('issueDate')}', expected '2026-03-18'")
            if inv.get("dueDate") != "2026-05-18":
                errors.append(f"Due date is '{inv.get('dueDate')}', expected '2026-05-18'")
            if inv.get("reference") != "WVV-2026-001":
                errors.append(f"Reference is '{inv.get('reference')}', expected 'WVV-2026-001'")

            lis = inv.get("lineItems", [])
            if len(lis) < 3:
                errors.append(f"Expected 3 line items, found {len(lis)}")
            else:
                tasting = next((l for l in lis if "tasting" in (l.get("description") or "").lower()
                                or "wine" in (l.get("description") or "").lower()), None)
                if not tasting:
                    errors.append("No wine tasting line item found")
                elif abs(tasting["quantity"] - 1) > 0.01 or abs(tasting["unitPrice"] - 2500) > 0.01:
                    errors.append(f"Tasting line: qty={tasting['quantity']} price={tasting['unitPrice']}, expected 1 x $2,500")

                tour = next((l for l in lis if "tour" in (l.get("description") or "").lower()
                             or "vineyard" in (l.get("description") or "").lower()), None)
                if not tour:
                    errors.append("No vineyard tour line item found")
                elif abs(tour["quantity"] - 2) > 0.01 or abs(tour["unitPrice"] - 600) > 0.01:
                    errors.append(f"Tour line: qty={tour['quantity']} price={tour['unitPrice']}, expected 2 x $600")

                gift = next((l for l in lis if "gift" in (l.get("description") or "").lower()
                             or "souvenir" in (l.get("description") or "").lower()), None)
                if not gift:
                    errors.append("No souvenir gift packs line item found")
                elif abs(gift["quantity"] - 20) > 0.01 or abs(gift["unitPrice"] - 45) > 0.01:
                    errors.append(f"Gift line: qty={gift['quantity']} price={gift['unitPrice']}, expected 20 x $45")

    if errors:
        return False, "; ".join(errors)
    return True, "Wairau Valley Vineyards created with approved AUD invoice"
