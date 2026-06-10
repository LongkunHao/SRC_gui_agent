"""Verify: Nelson contact — set draft ref to NELSON-PRIORITY-01, approve AA invoice."""
import requests


def verify(server_url: str) -> tuple[bool, str]:
    state = requests.get(f"{server_url}/api/state", timeout=5).json()
    invoices = state.get("invoices", [])
    errors = []

    # Nelson contact is Clearwater Environmental (con_17)
    # Draft invoice: inv_42 — reference should be updated
    inv_42 = next((i for i in invoices if i["id"] == "inv_42"), None)
    if not inv_42:
        errors.append("Invoice inv_42 not found")
    elif inv_42.get("reference") != "NELSON-PRIORITY-01":
        errors.append(f"inv_42 reference is '{inv_42.get('reference')}', expected 'NELSON-PRIORITY-01'")

    # AA invoice: inv_17 — should be approved
    inv_17 = next((i for i in invoices if i["id"] == "inv_17"), None)
    if not inv_17:
        errors.append("Invoice inv_17 not found")
    elif inv_17["status"] != "awaiting_payment":
        errors.append(f"inv_17 status is '{inv_17['status']}', expected 'awaiting_payment'")

    if errors:
        return False, "; ".join(errors)
    return True, "Nelson contact: inv_42 ref updated, inv_17 approved"
