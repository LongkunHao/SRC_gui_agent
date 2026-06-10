import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()

    # Check USD balance increased by at least $500
    balances = state.get("balances", [])
    usd_balance = None
    for bal in balances:
        if bal.get("currency") == "USD":
            usd_balance = bal
            break

    if usd_balance is None:
        return False, "No USD balance found."

    if usd_balance.get("amount", 0) < 3347.63:
        return False, f"USD balance is {usd_balance.get('amount')}, expected at least 3347.63 (2847.63 + 500)."

    # Check for transfer_in transaction referencing Chase
    transactions = state.get("transactions", [])
    found_transfer = False
    for txn in transactions:
        if txn.get("type") == "transfer_in":
            desc = txn.get("description", "")
            if "Chase" in desc:
                found_transfer = True
                break

    if not found_transfer:
        return False, "No transaction with type 'transfer_in' containing 'Chase' in description found."

    return True, "$500 added from Chase to USD balance successfully."
