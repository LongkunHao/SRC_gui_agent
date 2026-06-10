import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()

    balances = state.get("balances", [])

    usd_balance = None
    eur_balance = None
    for bal in balances:
        if bal.get("currency") == "USD":
            usd_balance = bal
        elif bal.get("currency") == "EUR":
            eur_balance = bal

    if usd_balance is None:
        return False, "No USD balance found."
    if eur_balance is None:
        return False, "No EUR balance found."

    # USD should have decreased from 2847.63
    if usd_balance.get("amount", 0) > 2747.63:
        return False, f"USD balance is {usd_balance.get('amount')}, expected at most 2747.63 (2847.63 - 100)."

    # EUR should have increased from 523.18
    if eur_balance.get("amount", 0) <= 523.18:
        return False, f"EUR balance is {eur_balance.get('amount')}, expected greater than 523.18 after conversion."

    # Check for currency_convert transaction
    transactions = state.get("transactions", [])
    found_convert = False
    for txn in transactions:
        if txn.get("type") == "currency_convert":
            found_convert = True
            break

    if not found_convert:
        return False, "No transaction with type 'currency_convert' found."

    return True, "$100 USD converted to EUR successfully."
