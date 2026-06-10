"""Verify: Approve all NZD awaiting-approval invoices, void non-NZD ones."""
import requests


def verify(server_url: str) -> tuple[bool, str]:
    state = requests.get(f"{server_url}/api/state", timeout=5).json()
    invoices = state.get("invoices", [])
    errors = []

    # NZD AA invoices that should be approved: inv_8, inv_17, inv_38, inv_56, inv_66, inv_77, inv_111
    approve_ids = ["inv_8", "inv_17", "inv_38", "inv_56", "inv_66", "inv_77", "inv_111"]
    for inv_id in approve_ids:
        inv = next((i for i in invoices if i["id"] == inv_id), None)
        if not inv:
            errors.append(f"Invoice {inv_id} not found")
        elif inv["status"] != "awaiting_payment":
            errors.append(f"{inv['invoiceNumber']} ({inv_id}) status is '{inv['status']}', expected 'awaiting_payment'")

    # AUD AA invoices that should be voided: inv_32, inv_45, inv_112
    void_ids = ["inv_32", "inv_45", "inv_112"]
    for inv_id in void_ids:
        inv = next((i for i in invoices if i["id"] == inv_id), None)
        if not inv:
            errors.append(f"Invoice {inv_id} not found")
        else:
            if inv["status"] != "voided":
                errors.append(f"{inv['invoiceNumber']} ({inv_id}) status is '{inv['status']}', expected 'voided'")
            if not inv.get("voidedAt"):
                errors.append(f"{inv_id} voidedAt is null")

    if errors:
        return False, "; ".join(errors)
    return True, "All 7 NZD AA invoices approved; all 3 non-NZD AA invoices voided"
