import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()

    errors = []

    debit_card = state.get("paypalDebitCard")
    if debit_card is None:
        return False, "No paypalDebitCard found in state."

    # Check cashBackEnabled == False
    if debit_card.get("cashBackEnabled") is not False:
        errors.append(
            f"paypalDebitCard.cashBackEnabled is {debit_card.get('cashBackEnabled')}, "
            f"expected False."
        )

    # Check directDeposit.enabled == False
    direct_deposit = debit_card.get("directDeposit")
    if direct_deposit is None:
        errors.append("paypalDebitCard.directDeposit is missing.")
    else:
        if direct_deposit.get("enabled") is not False:
            errors.append(
                f"paypalDebitCard.directDeposit.enabled is {direct_deposit.get('enabled')}, "
                f"expected False."
            )

    # Check dailySpendingLimit == 2000
    spending_limit = debit_card.get("dailySpendingLimit")
    if spending_limit is None:
        errors.append("paypalDebitCard.dailySpendingLimit is missing.")
    elif spending_limit != 2000:
        errors.append(
            f"paypalDebitCard.dailySpendingLimit is {spending_limit}, expected 2000."
        )

    if errors:
        return False, " ".join(errors)
    return True, "Successfully disabled cash back and direct deposit, and set spending limit to $2,000."
