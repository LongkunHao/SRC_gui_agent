"""Verify: Delete every draft invoice with total > $10,000."""
import requests


def verify(server_url: str) -> tuple[bool, str]:
    state = requests.get(f"{server_url}/api/state", timeout=5).json()
    invoices = state.get("invoices", [])
    errors = []

    # Draft invoices over $10k: inv_25 ($65,659), inv_42 ($39,775),
    # inv_61 ($64,760), inv_82 ($115,000), inv_93 ($27,968)
    deleted_ids = ["inv_25", "inv_42", "inv_61", "inv_82", "inv_93"]

    for inv_id in deleted_ids:
        inv = next((i for i in invoices if i["id"] == inv_id), None)
        if inv:
            errors.append(f"{inv['invoiceNumber']} ({inv_id}, total {inv['total']}) still exists, expected deleted")

    # Draft invoices under $10k should still exist
    kept_ids = ["inv_5", "inv_18", "inv_20", "inv_83", "inv_84", "inv_108"]
    for inv_id in kept_ids:
        inv = next((i for i in invoices if i["id"] == inv_id), None)
        if not inv:
            errors.append(f"{inv_id} was deleted but should not have been (total <= $10,000)")

    if errors:
        return False, "; ".join(errors)
    return True, f"All {len(deleted_ids)} draft invoices over $10,000 deleted; smaller drafts kept"
