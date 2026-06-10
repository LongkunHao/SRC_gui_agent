import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()

    errors = []

    # Plan with most remaining payments is Nike (3 remaining).
    # Next payment amount: $47.25.
    # Should have converted $47.25 USD to GBP.

    balances = state.get("balances", [])

    # GBP balance should have increased (from seed 189.42)
    gbp_bal = None
    for b in balances:
        if b.get("currency") == "GBP":
            gbp_bal = b
            break

    if gbp_bal is None:
        errors.append("GBP balance not found.")
    else:
        seed_gbp = 189.42
        if gbp_bal.get("amount", 0) <= seed_gbp:
            errors.append(
                f"GBP balance is {gbp_bal.get('amount')}, expected > {seed_gbp} "
                f"after converting $47.25 to GBP."
            )

    # USD balance should have decreased by ~$47.25 (from 2847.63)
    usd_bal = None
    for b in balances:
        if b.get("currency") == "USD":
            usd_bal = b
            break

    if usd_bal is None:
        errors.append("USD balance not found.")
    else:
        expected_usd = 2847.63 - 47.25
        if abs(usd_bal.get("amount", 0) - expected_usd) > 1.0:
            errors.append(
                f"USD balance is {usd_bal.get('amount')}, expected ~{expected_usd} "
                f"after converting $47.25."
            )

    # Should have a currency_convert transaction mentioning GBP
    transactions = state.get("transactions", [])
    found_convert = any(
        t.get("type") == "currency_convert" and "GBP" in (t.get("description") or "").upper()
        for t in transactions
    )
    if not found_convert:
        errors.append("No currency_convert transaction to GBP found.")

    if errors:
        return False, " ".join(errors)
    return True, "Converted Nike Pay in 4 next payment amount ($47.25) from USD to GBP."
