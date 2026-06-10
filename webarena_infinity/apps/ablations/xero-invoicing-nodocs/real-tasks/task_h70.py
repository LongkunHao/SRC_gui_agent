"""Verify: Earliest-due overdue invoice voided, new draft for same contact."""
import requests


def verify(server_url: str) -> tuple[bool, str]:
    state = requests.get(f"{server_url}/api/state", timeout=5).json()
    invoices = state.get("invoices", [])
    errors = []

    # Earliest due date among overdue: inv_87 Swift Courier (dueDate 2025-10-27)
    inv_87 = next((i for i in invoices if i["id"] == "inv_87"), None)
    if not inv_87:
        errors.append("INV-0087 not found")
    else:
        if inv_87["status"] != "voided":
            errors.append(f"INV-0087 status is '{inv_87['status']}', expected 'voided'")
        if not inv_87.get("voidedAt"):
            errors.append("INV-0087 voidedAt is null")

    # New draft invoice for Swift Courier Services (con_12)
    # Seed drafts for Swift Courier: none
    new_drafts = [i for i in invoices
                  if i.get("contactId") == "con_12" and i.get("status") == "draft"]
    if not new_drafts:
        errors.append("No new draft invoice found for Swift Courier Services (con_12)")
    else:
        inv = new_drafts[0]
        if inv.get("issueDate") != "2026-03-18":
            errors.append(f"New draft issueDate is '{inv.get('issueDate')}', expected '2026-03-18'")
        if inv.get("dueDate") != "2026-04-17":
            errors.append(f"New draft dueDate is '{inv.get('dueDate')}', expected '2026-04-17'")
        lis = inv.get("lineItems", [])
        if not lis:
            errors.append("New draft has no line items")
        else:
            li = lis[0]
            desc = (li.get("description") or "").lower()
            if "replacement" not in desc:
                errors.append(f"Line item description '{li.get('description')}' doesn't contain 'replacement'")
            if abs(li.get("quantity", 0) - 1) > 0.01 or abs(li.get("unitPrice", 0) - 1000) > 0.01:
                errors.append(f"Line item: qty={li.get('quantity')} price={li.get('unitPrice')}, expected 1 x $1,000")

    if errors:
        return False, "; ".join(errors)
    return True, "Earliest-due overdue (INV-0087) voided; new draft created for Swift Courier"
