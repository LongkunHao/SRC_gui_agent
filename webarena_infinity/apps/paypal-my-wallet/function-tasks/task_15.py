import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()

    balances = state.get("balances", [])
    chf_entry = None
    for b in balances:
        if b.get("currency") == "CHF":
            chf_entry = b
            break

    if chf_entry is None:
        return False, "No balance entry with currency 'CHF' found in balances array."

    if chf_entry.get("amount") != 0:
        return False, f"CHF balance amount should be 0, but got {chf_entry.get('amount')}."

    if chf_entry.get("isPrimary") not in (False, None):
        if chf_entry.get("isPrimary") is True:
            return False, "CHF balance isPrimary should be false, but it is true."

    if chf_entry.get("isPrimary") is True:
        return False, "CHF balance isPrimary should be false, but it is true."

    return True, "CHF currency was successfully added with amount 0 and isPrimary false."
