"""Verify: Void JOB- overdue invoices, update company address."""
import requests


def verify(server_url: str) -> tuple[bool, str]:
    state = requests.get(f"{server_url}/api/state", timeout=5).json()
    invoices = state.get("invoices", [])
    settings = state.get("settings", {})
    errors = []

    # JOB- overdue invoices: inv_33 (JOB-4455), inv_59 (JOB-4460)
    for inv_id in ["inv_33", "inv_59"]:
        inv = next((i for i in invoices if i["id"] == inv_id), None)
        if not inv:
            errors.append(f"Invoice {inv_id} not found")
            continue
        if inv["status"] != "voided":
            errors.append(f"{inv['invoiceNumber']} ({inv_id}) status is '{inv['status']}', expected 'voided'")
        if not inv.get("voidedAt"):
            errors.append(f"{inv_id} voidedAt is null")

    # Company address
    expected_addr = "50 Shortland Street, Level 15, Auckland 1010, New Zealand"
    if settings.get("companyAddress") != expected_addr:
        errors.append(f"companyAddress is '{settings.get('companyAddress')}', expected '{expected_addr}'")

    if errors:
        return False, "; ".join(errors)
    return True, "JOB- overdue invoices voided; company address updated"
