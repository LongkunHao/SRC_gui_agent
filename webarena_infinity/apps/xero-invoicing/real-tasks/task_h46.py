import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."

    state = resp.json()

    errors = []

    # All originally draft quotes should now be sent
    # QU-0025 was the only draft quote
    qu_0025 = next((q for q in state.get("quotes", []) if q.get("number") == "QU-0025"), None)
    if qu_0025 is None:
        errors.append("QU-0025 not found.")
    elif qu_0025.get("status") != "sent":
        errors.append(f"QU-0025 expected 'sent', got '{qu_0025.get('status')}'.")

    # All originally draft invoices should be approved (awaiting_payment)
    # INV-0058, INV-0059, INV-0060 were draft
    for inv_num in ["INV-0058", "INV-0059", "INV-0060"]:
        inv = next((i for i in state.get("invoices", []) if i.get("number") == inv_num), None)
        if inv is None:
            errors.append(f"{inv_num} not found.")
        elif inv.get("status") != "awaiting_payment":
            errors.append(f"{inv_num} expected 'awaiting_payment', got '{inv.get('status')}'.")

    if errors:
        return False, " ".join(errors)

    return True, "All draft quotes sent and all draft invoices approved."
