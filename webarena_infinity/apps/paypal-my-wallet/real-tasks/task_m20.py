import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()

    errors = []

    # Check USD balance increased by 750
    balances = state.get("balances", [])
    usd_balance = None
    for b in balances:
        if b.get("currency") == "USD":
            usd_balance = b.get("amount")
            break

    if usd_balance is None:
        errors.append("No USD balance found in state.")
    else:
        expected_usd = 2847.63 + 750
        if abs(usd_balance - expected_usd) > 5.0:
            errors.append(
                f"USD balance is {usd_balance}, expected approximately {expected_usd} "
                f"(original 2847.63 plus 750)."
            )

    # Check for transfer_in transaction containing "Chase"
    transactions = state.get("transactions", [])
    found_transfer = False
    for txn in transactions:
        if txn.get("type") == "transfer_in" and "Chase" in txn.get("description", ""):
            found_transfer = True
            break

    if not found_transfer:
        errors.append(
            "No transaction with type 'transfer_in' containing 'Chase' in description found."
        )

    if errors:
        return False, " ".join(errors)
    return True, "Successfully transferred $750 from Chase into PayPal: USD balance increased to ~3597.63 and transfer_in transaction recorded."
