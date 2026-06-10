import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."

    state = resp.json()
    contact = next((c for c in state["contacts"] if c["name"] == "Bright Spark Electrical"), None)
    if not contact:
        return False, "Contact 'Bright Spark Electrical' not found."

    ri = next(
        (r for r in state["repeatingInvoices"]
         if r["contactId"] == contact["id"] and r.get("id") not in
         ["rep_001", "rep_002", "rep_003", "rep_004", "rep_005"]),
        None
    )
    if not ri:
        # Try finding any new repeating invoice for this contact
        ri = next(
            (r for r in state["repeatingInvoices"] if r["contactId"] == contact["id"]),
            None
        )
        if not ri:
            return False, "No repeating invoice found for Bright Spark Electrical."

    if ri["frequency"] != "monthly":
        return False, f"Repeating invoice frequency is '{ri['frequency']}', expected 'monthly'."

    if ri["saveAs"] != "draft":
        return False, f"Repeating invoice saveAs is '{ri['saveAs']}', expected 'draft'."

    if len(ri.get("lineItems", [])) < 1:
        return False, "Repeating invoice has no line items."

    return True, "New monthly repeating invoice created for Bright Spark Electrical."
