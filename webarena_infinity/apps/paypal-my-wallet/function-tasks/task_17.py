import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()

    balances = state.get("balances", [])

    eur_entry = None
    usd_entry = None
    for b in balances:
        if b.get("currency") == "EUR":
            eur_entry = b
        elif b.get("currency") == "USD":
            usd_entry = b

    if eur_entry is None:
        return False, "No EUR balance entry found in balances array."

    if usd_entry is None:
        return False, "No USD balance entry found in balances array."

    if eur_entry.get("isPrimary") is not True:
        return False, f"EUR balance isPrimary should be true, but got {eur_entry.get('isPrimary')}."

    if usd_entry.get("isPrimary") is not False:
        return False, f"USD balance isPrimary should be false, but got {usd_entry.get('isPrimary')}."

    current_user = state.get("currentUser", {})
    primary_currency = current_user.get("primaryCurrency")
    if primary_currency != "EUR":
        return False, f"currentUser.primaryCurrency should be 'EUR', but got '{primary_currency}'."

    return True, "EUR is now set as the primary currency. USD isPrimary is false and currentUser.primaryCurrency is 'EUR'."
