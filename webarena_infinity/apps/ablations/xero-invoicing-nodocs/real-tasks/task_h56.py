"""Verify: Dunedin contact — delete draft, approve AA, pay AP."""
import requests


def verify(server_url: str) -> tuple[bool, str]:
    state = requests.get(f"{server_url}/api/state", timeout=5).json()
    invoices = state.get("invoices", [])
    payments = state.get("payments", [])
    errors = []

    # Dunedin contact: Heritage Craft Brewery (con_20)
    # Draft inv_20 should be deleted
    inv_20 = next((i for i in invoices if i["id"] == "inv_20"), None)
    if inv_20:
        errors.append(f"inv_20 still exists (status '{inv_20['status']}'), expected deleted")

    # AA inv_45 should be approved
    inv_45 = next((i for i in invoices if i["id"] == "inv_45"), None)
    if not inv_45:
        errors.append("Invoice inv_45 not found")
    elif inv_45["status"] != "awaiting_payment":
        errors.append(f"inv_45 status is '{inv_45['status']}', expected 'awaiting_payment'")

    # AP inv_70 should be fully paid
    inv_70 = next((i for i in invoices if i["id"] == "inv_70"), None)
    if not inv_70:
        errors.append("Invoice inv_70 not found")
    else:
        if inv_70["status"] != "paid":
            errors.append(f"inv_70 status is '{inv_70['status']}', expected 'paid'")
        if inv_70.get("amountDue", 1) > 0.01:
            errors.append(f"inv_70 amountDue is {inv_70.get('amountDue')}, expected 0")
        inv70_pays = [p for p in payments if p["invoiceId"] == "inv_70"]
        new_pays = [p for p in inv70_pays if p.get("bankAccountId") == "bank_1"]
        if not new_pays:
            errors.append("No Business Cheque payment found for inv_70")

    if errors:
        return False, "; ".join(errors)
    return True, "Dunedin contact: inv_20 deleted, inv_45 approved, inv_70 paid"
