import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()

    errors = []

    balances = state.get("balances", [])
    usd_balance = None
    gbp_balance = None
    for bal in balances:
        if bal.get("currency") == "USD":
            usd_balance = bal.get("amount")
        elif bal.get("currency") == "GBP":
            gbp_balance = bal.get("amount")

    # Check USD balance decreased from 2847.63
    if usd_balance is None:
        errors.append("USD balance not found in state.")
    else:
        if usd_balance >= 2847.63:
            errors.append(
                f"USD balance is {usd_balance}, expected it to have decreased from 2847.63 "
                f"after converting $150 to GBP."
            )
        # Should have decreased by 150
        expected_usd = 2697.63  # 2847.63 - 150
        if abs(usd_balance - expected_usd) > 1.0:
            errors.append(
                f"USD balance is {usd_balance}, expected ~{expected_usd} "
                f"(original 2847.63 minus 150 conversion)."
            )

    # Check GBP balance increased from 189.42
    if gbp_balance is None:
        errors.append("GBP balance not found in state.")
    else:
        if gbp_balance <= 189.42:
            errors.append(
                f"GBP balance is {gbp_balance}, expected it to have increased from 189.42 "
                f"after converting $150 to GBP."
            )

    # Check for a currency_convert transaction
    transactions = state.get("transactions", [])
    found_convert = False
    for txn in transactions:
        if txn.get("type") == "currency_convert":
            desc = (txn.get("description") or "").lower()
            if "gbp" in desc or "british" in desc:
                found_convert = True
                break
    # Also accept any currency_convert if USD decreased and GBP increased
    if not found_convert:
        for txn in transactions:
            if txn.get("type") == "currency_convert":
                found_convert = True
                break

    if not found_convert:
        errors.append(
            "No transaction with type 'currency_convert' found."
        )

    if errors:
        return False, " ".join(errors)
    return True, "Successfully converted $150 to British pounds."
