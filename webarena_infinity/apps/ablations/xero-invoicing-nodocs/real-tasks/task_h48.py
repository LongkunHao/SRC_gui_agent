"""Verify: Void every overdue invoice with total > $10,000."""
import requests


def verify(server_url: str) -> tuple[bool, str]:
    state = requests.get(f"{server_url}/api/state", timeout=5).json()
    invoices = state.get("invoices", [])
    errors = []

    # Overdue invoices with total > 10000:
    # inv_40 ($121,725), inv_102 ($60,975.88), inv_59 ($80,707),
    # inv_15 ($35,937.50), inv_63 ($14,921.25), inv_100 ($13,785)
    void_ids = ["inv_40", "inv_102", "inv_59", "inv_15", "inv_63", "inv_100"]

    for inv_id in void_ids:
        inv = next((i for i in invoices if i["id"] == inv_id), None)
        if not inv:
            errors.append(f"Invoice {inv_id} not found")
            continue
        if inv["status"] != "voided":
            errors.append(f"{inv['invoiceNumber']} ({inv_id}) status is '{inv['status']}', expected 'voided'")
        if not inv.get("voidedAt"):
            errors.append(f"{inv_id} voidedAt is null")

    # Overdue invoices with total <= 10000 should remain overdue
    keep_ids = ["inv_87", "inv_68", "inv_79", "inv_89", "inv_104", "inv_33", "inv_107", "inv_39"]
    for inv_id in keep_ids:
        inv = next((i for i in invoices if i["id"] == inv_id), None)
        if inv and inv["status"] == "voided":
            errors.append(f"{inv_id} (total {inv.get('total')}) was voided but should not have been (total <= $10,000)")

    if errors:
        return False, "; ".join(errors)
    return True, f"All {len(void_ids)} overdue invoices above $10,000 voided; smaller ones untouched"
