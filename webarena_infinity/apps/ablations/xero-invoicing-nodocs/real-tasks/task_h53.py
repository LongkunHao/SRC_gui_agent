"""Verify: Wellington contacts — last alphabetically (Nexus Technologies) overdue voided."""
import requests


def verify(server_url: str) -> tuple[bool, str]:
    state = requests.get(f"{server_url}/api/state", timeout=5).json()
    invoices = state.get("invoices", [])
    errors = []

    # Wellington contacts: Apex Legal Partners, Harmony Music Academy, Nexus Technologies Ltd
    # Alphabetically last: Nexus Technologies Ltd (con_4)
    # Their overdue invoices: inv_79, inv_104
    target_ids = ["inv_79", "inv_104"]

    for inv_id in target_ids:
        inv = next((i for i in invoices if i["id"] == inv_id), None)
        if not inv:
            errors.append(f"Invoice {inv_id} not found")
            continue
        if inv["status"] != "voided":
            errors.append(f"{inv['invoiceNumber']} ({inv_id}) status is '{inv['status']}', expected 'voided'")
        if not inv.get("voidedAt"):
            errors.append(f"{inv_id} voidedAt is null")

    # Other Wellington contacts' overdue invoices should NOT be voided
    # Harmony Music (con_13): inv_63 overdue
    inv_63 = next((i for i in invoices if i["id"] == "inv_63"), None)
    if inv_63 and inv_63["status"] == "voided":
        errors.append("inv_63 (Harmony Music) was voided but should not — wrong Wellington contact")

    # Apex Legal (con_18): inv_68 overdue
    inv_68 = next((i for i in invoices if i["id"] == "inv_68"), None)
    if inv_68 and inv_68["status"] == "voided":
        errors.append("inv_68 (Apex Legal) was voided but should not — wrong Wellington contact")

    if errors:
        return False, "; ".join(errors)
    return True, "Nexus Technologies (last alphabetically in Wellington) overdue invoices voided"
