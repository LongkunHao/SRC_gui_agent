import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."

    state = resp.json()

    cn = next((c for c in state["creditNotes"] if c["number"] == "CN-0012"), None)
    if not cn:
        return False, "Credit note CN-0012 not found."

    inv = next((i for i in state["invoices"] if i["number"] == "INV-0047"), None)
    if not inv:
        return False, "Invoice INV-0047 not found."

    # Check credit note allocation
    alloc = next((a for a in cn["allocations"] if a["invoiceNumber"] == "INV-0047"), None)
    if not alloc:
        return False, "No allocation found from CN-0012 to INV-0047."

    if abs(alloc["amount"] - 2035.00) > 0.01:
        return False, f"Allocation amount is {alloc['amount']}, expected 2035.00."

    # Check CN fully allocated
    if abs(cn["remainingCredit"]) > 0.01:
        return False, f"CN-0012 remainingCredit is {cn['remainingCredit']}, expected 0."

    if cn["status"] != "paid":
        return False, f"CN-0012 status is '{cn['status']}', expected 'paid'."

    # Check invoice amount due reduced
    expected_inv_due = 18652.70 - 2035.00
    if abs(inv["amountDue"] - expected_inv_due) > 0.01:
        return False, f"INV-0047 amountDue is {inv['amountDue']}, expected {expected_inv_due}."

    return True, "CN-0012 fully allocated ($2,035) to INV-0047."
