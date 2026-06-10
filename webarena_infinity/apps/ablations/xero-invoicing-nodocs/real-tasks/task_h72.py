"""Verify: PO-2025 invoices — AA approved, overdue voided."""
import requests


def verify(server_url: str) -> tuple[bool, str]:
    state = requests.get(f"{server_url}/api/state", timeout=5).json()
    invoices = state.get("invoices", [])
    errors = []

    # PO-2025 awaiting_approval: inv_77 → approved
    inv_77 = next((i for i in invoices if i["id"] == "inv_77"), None)
    if not inv_77:
        errors.append("INV-0077 not found")
    elif inv_77["status"] != "awaiting_payment":
        errors.append(f"INV-0077 status is '{inv_77['status']}', expected 'awaiting_payment'")

    # PO-2025 overdue: inv_102 → voided
    inv_102 = next((i for i in invoices if i["id"] == "inv_102"), None)
    if not inv_102:
        errors.append("INV-0102 not found")
    else:
        if inv_102["status"] != "voided":
            errors.append(f"INV-0102 status is '{inv_102['status']}', expected 'voided'")
        if not inv_102.get("voidedAt"):
            errors.append("INV-0102 voidedAt is null")

    if errors:
        return False, "; ".join(errors)
    return True, "PO-2025 invoices: AA approved, overdue voided"
