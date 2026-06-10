import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."

    state = resp.json()

    # CN-0009 is Coastal Living credit note ($249.75)
    cn = next((c for c in state.get("creditNotes", []) if c.get("number") == "CN-0009"), None)
    if cn is None:
        return False, "CN-0009 not found."

    # Check CN-0009 has allocation to INV-0049
    allocations = cn.get("allocations", [])
    alloc_to_049 = next(
        (a for a in allocations if a.get("invoiceNumber") == "INV-0049" or a.get("invoiceId") == "inv_008"),
        None
    )
    if alloc_to_049 is None:
        return False, "CN-0009 not allocated to INV-0049."

    # Check INV-0049 has a $2,000 payment
    inv = next((i for i in state.get("invoices", []) if i.get("number") == "INV-0049"), None)
    if inv is None:
        return False, "INV-0049 not found."

    payments = inv.get("payments", [])
    pay_2000 = next((p for p in payments if abs(p.get("amount", 0) - 2000.00) < 1.00), None)
    if pay_2000 is None:
        return False, "No $2,000 payment found on INV-0049."

    return True, "CN-0009 allocated to INV-0049 and $2,000 payment recorded."
