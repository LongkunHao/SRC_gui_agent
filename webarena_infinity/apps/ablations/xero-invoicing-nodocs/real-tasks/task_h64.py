"""Verify: Invoice prefix PAY-, next number 300, new drafts for Bay of Plenty contacts."""
import requests


def verify(server_url: str) -> tuple[bool, str]:
    state = requests.get(f"{server_url}/api/state", timeout=5).json()
    invoices = state.get("invoices", [])
    settings = state.get("settings", {})
    errors = []

    # Settings checks
    if settings.get("invoiceNumberPrefix") != "PAY-":
        errors.append(f"invoiceNumberPrefix is '{settings.get('invoiceNumberPrefix')}', expected 'PAY-'")
    if settings.get("invoiceNumberNextNumber") not in (302, 303):
        # After creating 2 invoices starting from 300, next should be 302
        actual = settings.get("invoiceNumberNextNumber")
        if actual != 302:
            errors.append(f"invoiceNumberNextNumber is {actual}, expected 302")

    # Bay of Plenty contacts: Pacific Timber (con_14), Pinnacle Construction (con_9)
    for con_id, con_name in [("con_14", "Pacific Timber Supplies"), ("con_9", "Pinnacle Construction Co")]:
        # Find new draft invoices (not in seed data)
        seed_draft_ids = {
            "con_14": set(),  # Pacific Timber has no seed drafts
            "con_9": {"inv_84"},  # Pinnacle has inv_84 as seed draft
        }
        new_drafts = [i for i in invoices
                      if i.get("contactId") == con_id
                      and i.get("status") == "draft"
                      and i["id"] not in seed_draft_ids[con_id]]
        if not new_drafts:
            errors.append(f"No new draft invoice found for {con_name} ({con_id})")
            continue
        inv = new_drafts[0]
        if inv.get("issueDate") != "2026-03-18":
            errors.append(f"{con_name} draft issueDate is '{inv.get('issueDate')}', expected '2026-03-18'")
        if inv.get("dueDate") != "2026-04-17":
            errors.append(f"{con_name} draft dueDate is '{inv.get('dueDate')}', expected '2026-04-17'")
        lis = inv.get("lineItems", [])
        if len(lis) < 1:
            errors.append(f"{con_name} draft has no line items")
        else:
            li = lis[0]
            desc = (li.get("description") or "").lower()
            if "regional" not in desc and "service" not in desc:
                errors.append(f"{con_name} draft line item description '{li.get('description')}' doesn't match 'Regional service fee'")
            if abs(li.get("quantity", 0) - 1) > 0.01 or abs(li.get("unitPrice", 0) - 500) > 0.01:
                errors.append(f"{con_name} draft line: qty={li.get('quantity')} price={li.get('unitPrice')}, expected 1 x $500")

    if errors:
        return False, "; ".join(errors)
    return True, "Prefix PAY-, next number 300+, new drafts for Bay of Plenty contacts"
