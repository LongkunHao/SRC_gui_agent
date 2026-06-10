import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()

    # Check USD balance decreased by at least $200
    balances = state.get("balances", [])
    usd_balance = None
    for bal in balances:
        if bal.get("currency") == "USD":
            usd_balance = bal
            break

    if usd_balance is None:
        return False, "No USD balance found."

    if usd_balance.get("amount", 0) > 2647.63:
        return False, f"USD balance is {usd_balance.get('amount')}, expected at most 2647.63 (2847.63 - 200)."

    # Check for transfer_out transaction referencing Bank of America
    transactions = state.get("transactions", [])
    found_transfer = False
    for txn in transactions:
        if txn.get("type") == "transfer_out":
            desc = txn.get("description", "")
            if "Bank of America" in desc:
                found_transfer = True
                break

    if not found_transfer:
        return False, "No transaction with type 'transfer_out' containing 'Bank of America' in description found."

    return True, "$200 withdrawn to Bank of America successfully."
