"""Verify: Rotorua contact overdue invoices paid, phone updated."""
import requests


def verify(server_url: str) -> tuple[bool, str]:
    state = requests.get(f"{server_url}/api/state", timeout=5).json()
    invoices = state.get("invoices", [])
    contacts = state.get("contacts", [])
    payments = state.get("payments", [])
    errors = []

    # Rotorua contact: Pacific Timber Supplies (con_14)
    con = next((c for c in contacts if c["id"] == "con_14"), None)
    if not con:
        errors.append("Pacific Timber Supplies (con_14) not found")
    else:
        if con.get("phone") != "+64 7 347 0000":
            errors.append(f"Phone is '{con.get('phone')}', expected '+64 7 347 0000'")

    # Overdue invoices: inv_39, inv_89
    for inv_id, inv_num in [("inv_39", "INV-0039"), ("inv_89", "INV-0089")]:
        inv = next((i for i in invoices if i["id"] == inv_id), None)
        if not inv:
            errors.append(f"{inv_num} not found")
            continue
        if inv["status"] != "paid":
            errors.append(f"{inv_num} status is '{inv['status']}', expected 'paid'")
        if inv.get("amountDue", 1) > 0.01:
            errors.append(f"{inv_num} amountDue is {inv.get('amountDue')}, expected 0")
        pays = [p for p in payments if p["invoiceId"] == inv_id]
        if not pays:
            errors.append(f"No payment found for {inv_num}")
        elif pays[-1].get("bankAccountId") != "bank_1":
            errors.append(f"{inv_num} payment uses '{pays[-1].get('bankAccountId')}', expected 'bank_1'")

    if errors:
        return False, "; ".join(errors)
    return True, "Pacific Timber (Rotorua) overdue invoices paid, phone updated"
