import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."

    state = resp.json()

    # CN-0011 is Pacific Freight draft credit note ($968)
    cn = next((c for c in state.get("creditNotes", []) if c.get("number") == "CN-0011"), None)
    if cn is None:
        return False, "CN-0011 not found."

    # Should be approved (not draft)
    if cn.get("status") == "draft":
        return False, "CN-0011 is still draft — should be approved."

    # Should have allocation to INV-0048 (Pacific Freight data migration)
    allocations = cn.get("allocations", [])
    alloc_to_048 = next(
        (a for a in allocations if a.get("invoiceNumber") == "INV-0048" or a.get("invoiceId") == "inv_007"),
        None
    )
    if alloc_to_048 is None:
        return False, "CN-0011 not allocated to INV-0048 (data migration invoice)."

    # INV-0048 amountDue should be reduced
    inv = next((i for i in state.get("invoices", []) if i.get("number") == "INV-0048"), None)
    if inv is None:
        return False, "INV-0048 not found."
    if inv.get("amountDue", 4180) >= 4180.00:
        return False, f"INV-0048 amountDue not reduced (got ${inv.get('amountDue'):.2f})."

    return True, "CN-0011 approved and allocated to INV-0048."
