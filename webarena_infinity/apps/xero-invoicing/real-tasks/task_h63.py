import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."

    state = resp.json()

    # The contact whose only quote was declined is Horizon Media (QU-0026 declined)
    horizon = next((c for c in state.get("contacts", []) if "Horizon" in c.get("name", "")), None)
    if horizon is None:
        return False, "Horizon Media contact not found."
    h_id = horizon.get("id")

    # Find new credit note for Horizon Media
    seed_cn_numbers = {"CN-0008", "CN-0009", "CN-0010", "CN-0011", "CN-0012"}
    new_cns = [
        cn for cn in state.get("creditNotes", [])
        if cn.get("contactId") == h_id
        and cn.get("number") not in seed_cn_numbers
        and cn.get("status") != "deleted"
    ]
    if not new_cns:
        return False, "No new credit note found for Horizon Media."

    cn = new_cns[0]

    # Check line item: 5 hours consulting at $250
    line_items = cn.get("lineItems", [])
    consult = next(
        (li for li in line_items
         if abs(li.get("quantity", 0) - 5) < 0.01
         and abs(li.get("unitPrice", 0) - 250.00) < 1.00),
        None
    )
    if consult is None:
        return False, "No line item with 5 hours at ~$250 (consulting)."

    # Should be approved (not draft)
    if cn.get("status") == "draft":
        return False, "Credit note should be approved (not draft)."

    return True, f"Credit note {cn.get('number')} for Horizon Media (5h consulting), approved."
