import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."

    state = resp.json()

    # Highest-value paid invoice is INV-0064 ($23,100) for NT Power Corp
    inv_0064 = next((i for i in state.get("invoices", []) if i.get("number") == "INV-0064"), None)
    if inv_0064 is None:
        return False, "INV-0064 not found."

    contact_id = inv_0064.get("contactId")
    original_total = inv_0064.get("total", 0)

    # Find new draft invoice for same contact with reference REBILL-2026
    seed_numbers = {
        "INV-0042", "INV-0043", "INV-0044", "INV-0045", "INV-0046", "INV-0047",
        "INV-0048", "INV-0049", "INV-0050", "INV-0051", "INV-0052", "INV-0053",
        "INV-0054", "INV-0055", "INV-0056", "INV-0057", "INV-0058", "INV-0059",
        "INV-0060", "INV-0061", "INV-0062", "INV-0063", "INV-0064", "INV-0065",
        "INV-0066",
    }
    copies = [
        i for i in state.get("invoices", [])
        if i.get("contactId") == contact_id
        and i.get("number") not in seed_numbers
        and i.get("status") == "draft"
        and i.get("reference") == "REBILL-2026"
    ]
    if not copies:
        return False, "No draft copy of INV-0064 found with reference 'REBILL-2026'."

    copy = copies[0]
    if abs(copy.get("total", 0) - original_total) > 1.00:
        return False, f"Copy total ${copy.get('total'):.2f} doesn't match original ${original_total:.2f}."

    return True, f"Highest-value paid invoice copied as {copy.get('number')} with reference 'REBILL-2026'."
