import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()

    errors = []

    # Check for transfer_in transaction from Chase
    transactions = state.get("transactions", [])
    found_transfer_in = False
    for txn in transactions:
        if txn.get("type") == "transfer_in":
            desc = (txn.get("description") or "").lower()
            if "chase" in desc:
                amount = txn.get("amount", 0)
                if abs(amount) >= 999 and abs(amount) <= 1001:
                    found_transfer_in = True
                    break

    if not found_transfer_in:
        errors.append(
            "No transfer_in transaction found with 'Chase' in the description "
            "and amount of ~$1,000."
        )

    # Check for currency_convert transaction (USD to EUR)
    found_convert = False
    for txn in transactions:
        if txn.get("type") == "currency_convert":
            desc = (txn.get("description") or "").upper()
            if "EUR" in desc:
                found_convert = True
                break

    if not found_convert:
        errors.append(
            "No currency_convert transaction found with 'EUR' in the description."
        )

    # Check EUR balance increased from 523.18
    balances = state.get("balances", [])
    eur_balance = None
    usd_balance = None
    for bal in balances:
        if bal.get("currency") == "EUR":
            eur_balance = bal.get("amount")
        if bal.get("currency") == "USD":
            usd_balance = bal.get("amount")

    if eur_balance is None:
        errors.append("EUR balance not found in state.")
    else:
        if eur_balance <= 523.18:
            errors.append(
                f"EUR balance is {eur_balance}, expected it to increase from 523.18 "
                f"after converting $500 to EUR."
            )

    # Check USD balance: 2847.63 + 1000 - 500 = 3347.63
    if usd_balance is None:
        errors.append("USD balance not found in state.")
    else:
        expected_usd = 3347.63
        if abs(usd_balance - expected_usd) > 5.0:
            errors.append(
                f"USD balance is {usd_balance}, expected ~{expected_usd} "
                f"(original 2847.63 plus 1000 transfer in minus 500 conversion)."
            )

    if errors:
        return False, " ".join(errors)
    return True, "Successfully added $1,000 from Chase and converted $500 to euros."
