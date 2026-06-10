import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()

    errors = []

    # INR should exist in balances with amount > 0
    balances = state.get("balances", [])
    inr_bal = None
    usd_bal = None
    for b in balances:
        if b.get("currency") == "INR":
            inr_bal = b
        if b.get("currency") == "USD":
            usd_bal = b

    if inr_bal is None:
        errors.append("Indian Rupee (INR) not found in balances.")
    elif inr_bal.get("amount", 0) <= 0:
        errors.append(
            f"INR balance is {inr_bal.get('amount')}, expected > 0 after conversion."
        )

    # USD should have decreased by ~$100
    if usd_bal is None:
        errors.append("USD balance not found.")
    else:
        expected_usd = round(2847.63 - 100, 2)
        if abs(usd_bal.get("amount", 0) - expected_usd) > 5.0:
            errors.append(
                f"USD balance is {usd_bal.get('amount')}, expected ~{expected_usd}."
            )

    # Check for currency_convert transaction with INR
    transactions = state.get("transactions", [])
    found_convert = False
    for t in transactions:
        if t.get("type") == "currency_convert":
            desc = (t.get("description") or "").upper()
            if "INR" in desc:
                found_convert = True
                break
    if not found_convert:
        errors.append("No currency_convert transaction with INR found.")

    # Currency conversion should be set to card_issuer
    prefs = state.get("walletPreferences", {})
    if prefs.get("currencyConversionOption") != "card_issuer":
        errors.append(
            f"Currency conversion option is '{prefs.get('currencyConversionOption')}', "
            f"expected 'card_issuer'."
        )

    if errors:
        return False, " ".join(errors)
    return True, "Added INR, converted $100, and set currency conversion to card issuer."
