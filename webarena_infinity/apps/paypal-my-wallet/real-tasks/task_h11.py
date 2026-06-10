import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()

    errors = []

    # Check CHF balance exists with amount > 0
    balances = state.get("balances", [])
    chf_balance = None
    usd_balance = None
    for bal in balances:
        if bal.get("currency") == "CHF":
            chf_balance = bal
        if bal.get("currency") == "USD":
            usd_balance = bal

    if chf_balance is None:
        errors.append("No CHF (Swiss Franc) balance found in state['balances'].")
    else:
        if chf_balance.get("amount", 0) <= 0:
            errors.append(
                f"CHF balance amount is {chf_balance.get('amount')}, expected > 0 "
                f"(should contain the converted amount)."
            )

    # Check USD balance decreased from 2847.63
    if usd_balance is None:
        errors.append("USD balance not found in state.")
    else:
        usd_amount = usd_balance.get("amount", 0)
        if usd_amount >= 2847.63:
            errors.append(
                f"USD balance is {usd_amount}, expected it to decrease from 2847.63 "
                f"after converting $300 to CHF."
            )
        expected_usd = 2847.63 - 300
        if abs(usd_amount - expected_usd) > 5.0:
            errors.append(
                f"USD balance is {usd_amount}, expected ~{expected_usd} "
                f"(original 2847.63 minus ~300 conversion)."
            )

    # Check for a currency_convert transaction containing "CHF"
    transactions = state.get("transactions", [])
    found_convert = False
    for txn in transactions:
        if txn.get("type") == "currency_convert":
            desc = (txn.get("description") or "").upper()
            if "CHF" in desc:
                found_convert = True
                break

    if not found_convert:
        errors.append(
            "No currency_convert transaction found with 'CHF' in the description."
        )

    if errors:
        return False, " ".join(errors)
    return True, "Successfully added Swiss Franc to wallet and converted $300 into CHF."
