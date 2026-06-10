"""Verify: Waikato contacts — delete drafts and approve AA invoices."""
import requests


def verify(server_url: str) -> tuple[bool, str]:
    state = requests.get(f"{server_url}/api/state", timeout=5).json()
    invoices = state.get("invoices", [])
    errors = []

    # Waikato contacts: Hamilton Plumbing (con_2), Velocity Sports (con_25)

    # Velocity Sports draft inv_25 should be deleted
    inv_25 = next((i for i in invoices if i["id"] == "inv_25"), None)
    if inv_25:
        errors.append(f"inv_25 still exists (status '{inv_25['status']}'), expected deleted")

    # Hamilton Plumbing AA inv_77 should be approved
    inv_77 = next((i for i in invoices if i["id"] == "inv_77"), None)
    if not inv_77:
        errors.append("Invoice inv_77 not found")
    elif inv_77["status"] != "awaiting_payment":
        errors.append(f"inv_77 status is '{inv_77['status']}', expected 'awaiting_payment'")

    if errors:
        return False, "; ".join(errors)
    return True, "Waikato contacts: inv_25 deleted, inv_77 approved"
