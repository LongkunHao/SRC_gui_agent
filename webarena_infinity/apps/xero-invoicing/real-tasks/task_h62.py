import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."

    state = resp.json()

    # QU-0024 (Atlas Engineering, $76,725) is the most expensive sent quote — should be declined
    qu_0024 = next((q for q in state.get("quotes", []) if q.get("number") == "QU-0024"), None)
    if qu_0024 is None:
        return False, "QU-0024 not found."
    if qu_0024.get("status") != "declined":
        return False, f"Expected QU-0024 status 'declined', got '{qu_0024.get('status')}'."

    # Find Atlas Engineering contact
    atlas = next((c for c in state.get("contacts", []) if "Atlas" in c.get("name", "")), None)
    if atlas is None:
        return False, "Atlas Engineering contact not found."
    atlas_id = atlas.get("id")

    # Find new quote for Atlas Engineering (not QU-0024)
    seed_numbers = {"QU-0022", "QU-0023", "QU-0024", "QU-0025", "QU-0026", "QU-0027", "QU-0028", "QU-0029"}
    new_quotes = [
        q for q in state.get("quotes", [])
        if q.get("contactId") == atlas_id
        and q.get("number") not in seed_numbers
        and q.get("status") != "deleted"
    ]
    if not new_quotes:
        return False, "No new quote found for Atlas Engineering."

    quo = new_quotes[0]
    line_items = quo.get("lineItems", [])

    # Check 100 hours development at $185
    dev_line = next(
        (li for li in line_items
         if abs(li.get("quantity", 0) - 100) < 0.01
         and abs(li.get("unitPrice", 0) - 185.00) < 1.00),
        None
    )
    if dev_line is None:
        return False, "No line item with 100 hours at ~$185 (development)."

    # Check 10 days project management at $1,400
    pm_line = next(
        (li for li in line_items
         if abs(li.get("quantity", 0) - 10) < 0.01
         and abs(li.get("unitPrice", 0) - 1400.00) < 1.00),
        None
    )
    if pm_line is None:
        return False, "No line item with 10 days at ~$1,400 (project management)."

    return True, f"QU-0024 declined, new quote {quo.get('number')} created for Atlas Engineering (100h dev + 10d PM)."
