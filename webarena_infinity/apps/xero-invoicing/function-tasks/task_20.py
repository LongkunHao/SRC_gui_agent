import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."

    state = resp.json()
    source = next((q for q in state["quotes"] if q["number"] == "QU-0024"), None)
    if not source:
        return False, "Source quote QU-0024 not found."

    copy = next((q for q in state["quotes"] if q["number"] == "QU-0030"), None)
    if not copy:
        return False, "Copied quote QU-0030 not found."

    if copy["status"] != "draft":
        return False, f"Copied quote status is '{copy['status']}', expected 'draft'."

    if copy["contactId"] != source["contactId"]:
        return False, f"Copied quote contactId '{copy['contactId']}' doesn't match source '{source['contactId']}'."

    if len(copy["lineItems"]) != len(source["lineItems"]):
        return False, f"Copied quote has {len(copy['lineItems'])} line items, expected {len(source['lineItems'])}."

    return True, "Quote QU-0024 copied to new draft QU-0030 successfully."
