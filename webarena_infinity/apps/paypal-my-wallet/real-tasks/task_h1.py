import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()

    errors = []

    # Check balances
    balances = state.get("balances")
    if not balances:
        return False, "No balances found in state."

    eur_bal = None
    jpy_bal = None
    for b in balances:
        if b.get("currency") == "EUR":
            eur_bal = b
        elif b.get("currency") == "JPY":
            jpy_bal = b

    if eur_bal is None:
        errors.append("EUR balance not found.")
    else:
        expected_eur = round(523.18 - 200, 2)
        actual_eur = eur_bal.get("amount", 0)
        if abs(actual_eur - expected_eur) > 1.0:
            errors.append(
                f"EUR balance is {actual_eur}, expected approximately {expected_eur} "
                f"(seed 523.18 minus 200)."
            )

    if jpy_bal is None:
        errors.append("JPY balance not found.")
    else:
        actual_jpy = jpy_bal.get("amount", 0)
        if actual_jpy <= 45200:
            errors.append(
                f"JPY balance is {actual_jpy}, expected it to have increased from seed value 45200."
            )

    # Check for currency_convert transaction
    transactions = state.get("transactions", [])
    convert_txn = None
    for t in transactions:
        if t.get("type") == "currency_convert":
            desc = t.get("description", "").lower()
            if "eur" in desc and "jpy" in desc:
                convert_txn = t
                break

    if convert_txn is None:
        # Also accept any currency_convert transaction that wasn't in seed data
        # Seed had one convert txn (txn_018) for USD to EUR. Look for a new one.
        for t in transactions:
            if t.get("type") == "currency_convert" and t.get("id") != "txn_018":
                convert_txn = t
                break

    if convert_txn is None:
        errors.append("No new currency_convert transaction found for EUR to JPY conversion.")

    if errors:
        return False, " ".join(errors)
    return True, "Successfully converted 200 EUR to JPY. EUR balance decreased and JPY balance increased."
