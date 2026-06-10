import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."

    state = resp.json()
    source = next((i for i in state["invoices"] if i["number"] == "INV-0046"), None)
    if not source:
        return False, "Source invoice INV-0046 not found."

    copy = next((i for i in state["invoices"] if i["number"] == "INV-0067"), None)
    if not copy:
        return False, "Copied invoice INV-0067 not found."

    if copy["status"] != "draft":
        return False, f"Copied invoice status is '{copy['status']}', expected 'draft'."

    if copy["contactId"] != source["contactId"]:
        return False, f"Copied invoice contactId '{copy['contactId']}' doesn't match source '{source['contactId']}'."

    if len(copy["lineItems"]) != len(source["lineItems"]):
        return False, f"Copied invoice has {len(copy['lineItems'])} line items, expected {len(source['lineItems'])}."

    return True, "Invoice INV-0046 copied to new draft INV-0067 successfully."
