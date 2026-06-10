"""Verify: Most expensive paid DataFlow invoice copied as draft with reference RENEWAL-2026."""
import requests


def verify(server_url: str) -> tuple[bool, str]:
    state = requests.get(f"{server_url}/api/state", timeout=5).json()
    invoices = state.get("invoices", [])
    errors = []

    # Most expensive paid DataFlow invoice: inv_86 ($53,216.25)
    # New draft for DataFlow (con_11) with reference RENEWAL-2026
    # Seed drafts for DataFlow: inv_61
    new_drafts = [i for i in invoices
                  if i.get("contactId") == "con_11"
                  and i.get("status") == "draft"
                  and i["id"] != "inv_61"]
    if not new_drafts:
        errors.append("No new draft invoice found for DataFlow Analytics (con_11)")
    else:
        inv = next((i for i in new_drafts if i.get("reference") == "RENEWAL-2026"), None)
        if not inv:
            inv = new_drafts[0]
            if inv.get("reference") != "RENEWAL-2026":
                errors.append(f"New draft reference is '{inv.get('reference')}', expected 'RENEWAL-2026'")

        # Verify line items match inv_86 (copied)
        lis = inv.get("lineItems", [])
        if len(lis) < 3:
            errors.append(f"Expected at least 3 line items (copied from INV-0086), found {len(lis)}")
        else:
            catering = next((l for l in lis if "catering" in (l.get("description") or "").lower()), None)
            if not catering:
                errors.append("No 'Catering services' line item found")
            elif abs(catering.get("quantity", 0) - 100) > 0.01 or abs(catering.get("unitPrice", 0) - 450) > 0.01:
                errors.append(f"Catering line: qty={catering.get('quantity')} price={catering.get('unitPrice')}, expected 100 x $450")

    if errors:
        return False, "; ".join(errors)
    return True, "DataFlow inv_86 copied as draft with reference RENEWAL-2026"
