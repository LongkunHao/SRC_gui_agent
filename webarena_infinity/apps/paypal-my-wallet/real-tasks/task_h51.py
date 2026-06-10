import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()

    errors = []

    # Seed credit balance is $1245.67. Half rounded down = $622.
    credit = state.get("paypalCredit")
    if credit is None:
        return False, "PayPal Credit not found."

    expected_balance = 1245.67 - 622
    if abs(credit.get("currentBalance", 0) - expected_balance) > 1.0:
        errors.append(
            f"PayPal Credit balance is {credit.get('currentBalance')}, "
            f"expected ~{expected_balance} after paying $622."
        )

    if credit.get("lastPaymentAmount") != 622:
        errors.append(
            f"Last payment amount is {credit.get('lastPaymentAmount')}, expected 622."
        )

    # USD balance should have decreased by $622
    balances = state.get("balances", [])
    usd_bal = None
    for b in balances:
        if b.get("currency") == "USD":
            usd_bal = b
            break

    if usd_bal is None:
        errors.append("USD balance not found.")
    else:
        expected_usd = 2847.63 - 622
        if abs(usd_bal.get("amount", 0) - expected_usd) > 5.0:
            errors.append(
                f"USD balance is {usd_bal.get('amount')}, expected ~{expected_usd}."
            )

    if errors:
        return False, " ".join(errors)
    return True, "Paid exactly half of PayPal Credit balance ($622) rounded down."
