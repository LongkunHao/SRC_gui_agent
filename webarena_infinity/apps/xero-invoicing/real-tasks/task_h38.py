import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."

    state = resp.json()
    invoices = state.get("invoices", [])

    # INV-0050: Alpha Logistics supply chain ($13,255)
    inv_050 = next((i for i in invoices if i.get("number") == "INV-0050"), None)
    if inv_050 is None:
        return False, "Invoice INV-0050 not found."
    if inv_050.get("status") != "paid":
        return False, f"Expected INV-0050 status 'paid', got '{inv_050.get('status')}'."
    if abs(inv_050.get("amountDue", 9999)) > 0.01:
        return False, f"Expected INV-0050 amountDue=0, got {inv_050.get('amountDue')}."

    # INV-0051: Summit Health Group license ($6,060)
    inv_051 = next((i for i in invoices if i.get("number") == "INV-0051"), None)
    if inv_051 is None:
        return False, "Invoice INV-0051 not found."
    if inv_051.get("status") != "paid":
        return False, f"Expected INV-0051 status 'paid', got '{inv_051.get('status')}'."
    if abs(inv_051.get("amountDue", 9999)) > 0.01:
        return False, f"Expected INV-0051 amountDue=0, got {inv_051.get('amountDue')}."

    return True, "Both INV-0050 (Alpha Logistics) and INV-0051 (Summit Health) fully paid."
