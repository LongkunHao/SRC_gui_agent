import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."

    state = resp.json()
    contact = next((c for c in state["contacts"] if c["name"] == "Southern Cross Veterinary"), None)
    if not contact:
        return False, "Contact 'Southern Cross Veterinary' not found."

    ri = next(
        (r for r in state["repeatingInvoices"] if r["contactId"] == contact["id"]),
        None
    )
    if not ri:
        return False, "No repeating invoice found for Southern Cross Veterinary."

    if ri["frequency"] != "quarterly":
        return False, f"Repeating invoice frequency is '{ri['frequency']}', expected 'quarterly'."

    if ri["saveAs"] != "approved":
        return False, f"Repeating invoice saveAs is '{ri['saveAs']}', expected 'approved'."

    if len(ri.get("lineItems", [])) < 1:
        return False, "Repeating invoice has no line items."

    return True, "New quarterly repeating invoice created for Southern Cross Veterinary with approved save-as."
