import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."

    state = resp.json()

    cn = next((c for c in state["creditNotes"] if c["number"] == "CN-0009"), None)
    if not cn:
        return False, "Credit note CN-0009 not found."

    inv = next((i for i in state["invoices"] if i["number"] == "INV-0049"), None)
    if not inv:
        return False, "Invoice INV-0049 not found."

    # Check credit note allocation
    if len(cn["allocations"]) < 1:
        return False, "Credit note CN-0009 has no allocations."

    alloc = next((a for a in cn["allocations"] if a["invoiceNumber"] == "INV-0049"), None)
    if not alloc:
        return False, "No allocation found from CN-0009 to INV-0049."

    if abs(alloc["amount"] - 249.75) > 0.01:
        return False, f"Allocation amount is {alloc['amount']}, expected 249.75."

    # Check credit note remaining credit
    if abs(cn["remainingCredit"]) > 0.01:
        return False, f"CN-0009 remainingCredit is {cn['remainingCredit']}, expected 0."

    # Check credit note status (should be fully allocated = paid)
    if cn["status"] != "paid":
        return False, f"CN-0009 status is '{cn['status']}', expected 'paid'."

    # Check invoice amount due reduced
    expected_inv_due = 3715.00 - 249.75
    if abs(inv["amountDue"] - expected_inv_due) > 0.01:
        return False, f"INV-0049 amountDue is {inv['amountDue']}, expected {expected_inv_due}."

    return True, "CN-0009 fully allocated ($249.75) to INV-0049."
