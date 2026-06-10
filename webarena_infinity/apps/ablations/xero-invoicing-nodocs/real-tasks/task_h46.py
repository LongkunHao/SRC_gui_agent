"""Verify: Bay of Plenty — alphabetically first contact's overdue invoices paid."""
import requests


def verify(server_url: str) -> tuple[bool, str]:
    state = requests.get(f"{server_url}/api/state", timeout=5).json()
    invoices = state.get("invoices", [])
    payments = state.get("payments", [])
    errors = []

    # Bay of Plenty contacts: Pacific Timber Supplies (con_14), Pinnacle Construction Co (con_9)
    # Alphabetically first: Pacific Timber Supplies
    # Their overdue invoices: inv_39 ($4,027.50), inv_89 ($5,209)
    target_ids = ["inv_39", "inv_89"]

    for inv_id in target_ids:
        inv = next((i for i in invoices if i["id"] == inv_id), None)
        if not inv:
            errors.append(f"Invoice {inv_id} not found")
            continue
        if inv["status"] != "paid":
            errors.append(f"{inv['invoiceNumber']} ({inv_id}) status is '{inv['status']}', expected 'paid'")
        if inv.get("amountDue", 1) > 0.01:
            errors.append(f"{inv_id} amountDue is {inv.get('amountDue')}, expected 0")
        inv_pays = [p for p in payments if p["invoiceId"] == inv_id]
        new_pays = [p for p in inv_pays if p.get("bankAccountId") == "bank_1"]
        if not new_pays:
            errors.append(f"No Business Cheque payment found for {inv_id}")

    # Pinnacle Construction (con_9) overdue inv_59 should NOT be paid by this task
    inv_59 = next((i for i in invoices if i["id"] == "inv_59"), None)
    if inv_59 and inv_59["status"] == "paid":
        errors.append("inv_59 (Pinnacle Construction) was paid but should not have been — wrong Bay of Plenty contact")

    if errors:
        return False, "; ".join(errors)
    return True, "Pacific Timber Supplies (alphabetically first in Bay of Plenty) overdue invoices paid"
