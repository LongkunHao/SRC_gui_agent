"""Verify: AUD awaiting-approval invoices approved, AUD overdue invoices voided."""
import requests


def verify(server_url: str) -> tuple[bool, str]:
    state = requests.get(f"{server_url}/api/state", timeout=5).json()
    invoices = state.get("invoices", [])
    errors = []

    # AUD awaiting_approval → approved (awaiting_payment)
    for inv_id, inv_num in [("inv_32", "INV-0032"), ("inv_45", "INV-0045"), ("inv_112", "INV-0112")]:
        inv = next((i for i in invoices if i["id"] == inv_id), None)
        if not inv:
            errors.append(f"{inv_num} not found")
            continue
        if inv["status"] != "awaiting_payment":
            errors.append(f"{inv_num} status is '{inv['status']}', expected 'awaiting_payment'")

    # AUD overdue → voided
    for inv_id, inv_num in [("inv_33", "INV-0033"), ("inv_102", "INV-0102")]:
        inv = next((i for i in invoices if i["id"] == inv_id), None)
        if not inv:
            errors.append(f"{inv_num} not found")
            continue
        if inv["status"] != "voided":
            errors.append(f"{inv_num} status is '{inv['status']}', expected 'voided'")
        if not inv.get("voidedAt"):
            errors.append(f"{inv_num} voidedAt is null")

    if errors:
        return False, "; ".join(errors)
    return True, "All AUD awaiting-approval approved; all AUD overdue voided"
