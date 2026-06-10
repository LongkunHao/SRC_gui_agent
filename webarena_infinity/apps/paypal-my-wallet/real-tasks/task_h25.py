import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()

    errors = []

    balances = state.get("balances", [])
    aud_bal = None
    eur_bal = None
    for b in balances:
        if b.get("currency") == "AUD":
            aud_bal = b
        if b.get("currency") == "EUR":
            eur_bal = b

    # AUD should be ~0 (all converted)
    if aud_bal is not None and aud_bal.get("amount", 0) > 1.0:
        errors.append(
            f"AUD balance is {aud_bal.get('amount')}, expected ~0 after converting all."
        )

    # EUR should have increased from seed 523.18
    if eur_bal is None:
        errors.append("EUR balance not found.")
    else:
        if eur_bal.get("amount", 0) <= 523.18:
            errors.append(
                f"EUR balance is {eur_bal.get('amount')}, expected > 523.18 "
                f"(seed value) after converting AUD."
            )

    # Check for a currency_convert transaction AUD to EUR
    transactions = state.get("transactions", [])
    found_convert = False
    for t in transactions:
        if t.get("type") == "currency_convert":
            desc = (t.get("description") or "").upper()
            if "AUD" in desc and "EUR" in desc:
                found_convert = True
                break
    if not found_convert:
        errors.append("No currency_convert transaction from AUD to EUR found.")

    if errors:
        return False, " ".join(errors)
    return True, "Successfully converted all Australian dollars to euros."
