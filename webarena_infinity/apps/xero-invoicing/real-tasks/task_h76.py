import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."

    state = resp.json()

    # QU-0025 (Fresh Start Catering, was draft) -> should now be sent
    qu_0025 = next((q for q in state.get("quotes", []) if q.get("number") == "QU-0025"), None)
    if qu_0025 is None:
        return False, "QU-0025 not found."
    if qu_0025.get("status") != "sent":
        return False, f"Expected QU-0025 status 'sent', got '{qu_0025.get('status')}'."

    # Find Metro Fabrication Works
    metro = next((c for c in state.get("contacts", []) if "Metro" in c.get("name", "")), None)
    if metro is None:
        return False, "Metro Fabrication Works contact not found."
    metro_id = metro.get("id")

    # Find new quote for Metro Fabrication (copy of QU-0025)
    seed_numbers = {"QU-0022", "QU-0023", "QU-0024", "QU-0025", "QU-0026", "QU-0027", "QU-0028", "QU-0029"}
    new_quotes = [
        q for q in state.get("quotes", [])
        if q.get("contactId") == metro_id
        and q.get("number") not in seed_numbers
        and q.get("status") != "deleted"
    ]
    if not new_quotes:
        return False, "No new quote found for Metro Fabrication (copy with changed contact)."

    copy = new_quotes[0]

    # Copy should be a draft
    if copy.get("status") != "draft":
        return False, f"Expected copy status 'draft', got '{copy.get('status')}'."

    return True, f"QU-0025 sent, copy {copy.get('number')} created for Metro Fabrication Works."
