import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."

    state = resp.json()

    # Contact on Pitt Street: CloudNine Analytics (101 Pitt Street)
    cloudnine = next(
        (c for c in state.get("contacts", [])
         if "Pitt" in c.get("address", "")),
        None
    )
    if cloudnine is None:
        return False, "No contact found on Pitt Street."

    # Two invoices: INV-0047 (due 2026-02-15) and INV-0062 (due 2026-03-06)
    inv_0047 = next((i for i in state.get("invoices", []) if i.get("number") == "INV-0047"), None)
    inv_0062 = next((i for i in state.get("invoices", []) if i.get("number") == "INV-0062"), None)

    if inv_0047 is None:
        return False, "INV-0047 not found."
    if inv_0062 is None:
        return False, "INV-0062 not found."

    # INV-0047 has earlier due date (2/15) -> should be paid
    if inv_0047.get("status") != "paid":
        return False, f"Expected INV-0047 (earlier due date) status 'paid', got '{inv_0047.get('status')}'."

    if inv_0047.get("amountDue", 1) > 0.01:
        return False, f"INV-0047 still has outstanding balance: ${inv_0047.get('amountDue', 0):.2f}."

    # INV-0062 (later due date) -> should be voided
    if inv_0062.get("status") != "voided":
        return False, f"Expected INV-0062 (later due date) status 'voided', got '{inv_0062.get('status')}'."

    return True, "INV-0047 (earlier due) paid in full, INV-0062 (later due) voided."
