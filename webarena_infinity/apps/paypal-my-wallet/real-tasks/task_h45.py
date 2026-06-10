import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()

    errors = []

    # Minimum payment due on credit is $35 (seed).
    # Agent should withdraw $35 from savings, then pay $35 on credit.

    # Check savings decreased by $35 (from 12450.82 to ~12415.82)
    savings = state.get("savingsAccount")
    if savings is None:
        errors.append("Savings account not found.")
    else:
        expected_savings = 12450.82 - 35
        if abs(savings.get("balance", 0) - expected_savings) > 1.0:
            errors.append(
                f"Savings balance is {savings.get('balance')}, expected ~{expected_savings} "
                f"after withdrawing $35."
            )

    # Check credit balance decreased by $35 (from 1245.67 to ~1210.67)
    credit = state.get("paypalCredit")
    if credit is None:
        errors.append("PayPal Credit not found.")
    else:
        expected_credit = 1245.67 - 35
        if abs(credit.get("currentBalance", 0) - expected_credit) > 1.0:
            errors.append(
                f"PayPal Credit balance is {credit.get('currentBalance')}, "
                f"expected ~{expected_credit} after paying $35."
            )
        if credit.get("lastPaymentAmount") != 35:
            errors.append(
                f"Last payment amount is {credit.get('lastPaymentAmount')}, expected 35."
            )

    if errors:
        return False, " ".join(errors)
    return True, "Withdrew minimum payment ($35) from savings and paid PayPal Credit minimum."
