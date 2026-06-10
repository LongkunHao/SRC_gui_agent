import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()

    errors = []

    balances = state.get("balances", [])
    nok_bal = None
    eur_bal = None
    for b in balances:
        if b.get("currency") == "NOK":
            nok_bal = b
        if b.get("currency") == "EUR":
            eur_bal = b

    # NOK should exist and have a positive balance
    if nok_bal is None:
        errors.append("Norwegian Krone (NOK) not found in balances.")
    elif nok_bal.get("amount", 0) <= 0:
        errors.append(
            f"NOK balance is {nok_bal.get('amount')}, expected > 0 after conversion."
        )

    # EUR should have decreased from seed 523.18
    if eur_bal is None:
        errors.append("EUR balance not found.")
    else:
        if eur_bal.get("amount", 0) >= 523.18:
            errors.append(
                f"EUR balance is {eur_bal.get('amount')}, expected < 523.18 "
                f"after converting 100 EUR to NOK."
            )
        expected_eur = round(523.18 - 100, 2)
        if abs(eur_bal.get("amount", 0) - expected_eur) > 5.0:
            errors.append(
                f"EUR balance is {eur_bal.get('amount')}, expected ~{expected_eur}."
            )

    # Check for a currency_convert transaction EUR to NOK
    transactions = state.get("transactions", [])
    found_convert = False
    for t in transactions:
        if t.get("type") == "currency_convert":
            desc = (t.get("description") or "").upper()
            if "EUR" in desc and "NOK" in desc:
                found_convert = True
                break
    if not found_convert:
        errors.append("No currency_convert transaction from EUR to NOK found.")

    if errors:
        return False, " ".join(errors)
    return True, "Successfully added Norwegian Krone and converted 100 EUR into it."
