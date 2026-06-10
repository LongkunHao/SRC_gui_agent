"""Verify: Pay INV-0039, create new approved invoice for Pacific Timber Supplies."""
import requests


def verify(server_url: str) -> tuple[bool, str]:
    state = requests.get(f"{server_url}/api/state", timeout=5).json()
    invoices = state.get("invoices", [])
    payments = state.get("payments", [])
    errors = []

    # INV-0039 (inv_39) should be fully paid
    inv_39 = next((i for i in invoices if i["id"] == "inv_39"), None)
    if not inv_39:
        errors.append("Invoice inv_39 not found")
    else:
        if inv_39["status"] != "paid":
            errors.append(f"INV-0039 status is '{inv_39['status']}', expected 'paid'")
        if inv_39.get("amountDue", 1) > 0.01:
            errors.append(f"INV-0039 amountDue is {inv_39.get('amountDue')}, expected 0")
        inv39_pays = [p for p in payments if p["invoiceId"] == "inv_39"
                      and p.get("bankAccountId") == "bank_1"]
        if not inv39_pays:
            errors.append("No Business Cheque payment found for INV-0039")

    # New invoice for Pacific Timber Supplies (con_14)
    con_14_invoices = [i for i in invoices if i.get("contactId") == "con_14"]
    seed_ids = {"inv_14", "inv_39", "inv_64", "inv_89"}
    new_invoices = [i for i in con_14_invoices if i["id"] not in seed_ids]

    if not new_invoices:
        errors.append("No new invoice found for Pacific Timber Supplies (con_14)")
    else:
        inv = new_invoices[0]
        if inv.get("status") != "awaiting_payment":
            errors.append(f"New invoice status is '{inv.get('status')}', expected 'awaiting_payment'")
        if inv.get("issueDate") != "2026-03-18":
            errors.append(f"Issue date is '{inv.get('issueDate')}', expected '2026-03-18'")
        if inv.get("dueDate") != "2026-04-17":
            errors.append(f"Due date is '{inv.get('dueDate')}', expected '2026-04-17'")

        lis = inv.get("lineItems", [])
        followup = next((l for l in lis if "follow" in (l.get("description") or "").lower()
                         or "consult" in (l.get("description") or "").lower()), None)
        if not followup:
            errors.append("No 'Follow-up consulting' line item found")
        elif abs(followup["quantity"] - 10) > 0.01 or abs(followup["unitPrice"] - 200) > 0.01:
            errors.append(f"Follow-up line: qty={followup['quantity']} price={followup['unitPrice']}, expected 10 x $200")

    if errors:
        return False, "; ".join(errors)
    return True, "INV-0039 paid; new approved invoice created for Pacific Timber Supplies"
