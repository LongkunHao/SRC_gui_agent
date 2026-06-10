import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."

    state = resp.json()
    contact = next((c for c in state["contacts"] if c["name"] == "CloudNine Analytics"), None)
    if not contact:
        return False, "Contact 'CloudNine Analytics' not found."

    ri = next((r for r in state["repeatingInvoices"] if r["id"] == "rep_002"), None)
    if not ri:
        return False, "Repeating invoice rep_002 not found."

    if ri["frequency"] != "quarterly":
        return False, f"Repeating invoice frequency is '{ri['frequency']}', expected 'quarterly'."

    return True, "Repeating invoice for CloudNine Analytics changed to quarterly."
