import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()

    errors = []

    balances = state.get("balances", [])

    # JPY should be removed from balances
    jpy_bal = None
    usd_bal = None
    for b in balances:
        if b.get("currency") == "JPY":
            jpy_bal = b
        if b.get("currency") == "USD":
            usd_bal = b

    if jpy_bal is not None:
        if jpy_bal.get("amount", 0) > 1.0:
            errors.append(
                f"JPY balance still has {jpy_bal.get('amount')}, expected it to be "
                f"converted to USD first and then removed."
            )
        else:
            errors.append(
                "JPY currency still exists in balances (should be removed after conversion)."
            )

    # USD balance should have increased (seed JPY was 45200 yen ~ $302 USD)
    if usd_bal is None:
        errors.append("USD balance not found.")
    else:
        # 45200 JPY / 149.50 rate = ~$302.34 USD, minus 3% fee ~ $293
        # So USD should be > 2847.63 + ~280 = ~3127
        if usd_bal.get("amount", 0) <= 2847.63:
            errors.append(
                f"USD balance is {usd_bal.get('amount')}, expected > 2847.63 "
                f"after converting JPY to USD."
            )

    # Check for a currency_convert transaction JPY to USD
    transactions = state.get("transactions", [])
    found_convert = False
    for t in transactions:
        if t.get("type") == "currency_convert":
            desc = (t.get("description") or "").upper()
            if "JPY" in desc and "USD" in desc:
                found_convert = True
                break
    if not found_convert:
        errors.append("No currency_convert transaction from JPY to USD found.")

    if errors:
        return False, " ".join(errors)
    return True, "Successfully converted all JPY to USD and removed yen currency."
