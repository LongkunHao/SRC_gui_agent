import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()

    errors = []

    pc = state.get("paypalCredit")
    if pc is None:
        return False, "No paypalCredit found in state."

    # Credit balance should be 0 (paid off entirely from seed 1245.67)
    if pc.get("currentBalance", 0) > 1.0:
        errors.append(
            f"PayPal Credit balance is {pc.get('currentBalance')}, expected 0 "
            f"(paid off from seed balance of 1245.67)."
        )

    # Available credit should be close to full limit (5000)
    if pc.get("availableCredit", 0) < 4990:
        errors.append(
            f"Available credit is {pc.get('availableCredit')}, expected ~5000."
        )

    # Autopay should be set to 'full'
    if pc.get("autopayAmount") != "full":
        errors.append(
            f"Autopay amount is '{pc.get('autopayAmount')}', expected 'full'."
        )

    # Autopay should be enabled
    if pc.get("autopayEnabled") is not True:
        errors.append(
            f"Autopay is not enabled."
        )

    # USD balance should have decreased by ~1245.67
    balances = state.get("balances", [])
    usd_bal = None
    for b in balances:
        if b.get("currency") == "USD":
            usd_bal = b
            break

    if usd_bal is None:
        errors.append("USD balance not found.")
    else:
        expected_usd = round(2847.63 - 1245.67, 2)
        if abs(usd_bal.get("amount", 0) - expected_usd) > 5.0:
            errors.append(
                f"USD balance is {usd_bal.get('amount')}, expected ~{expected_usd}."
            )

    if errors:
        return False, " ".join(errors)
    return True, "PayPal Credit paid off and autopay set to full statement balance."
