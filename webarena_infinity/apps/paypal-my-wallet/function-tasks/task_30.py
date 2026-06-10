import requests


SEED_BALANCE = 1245.67
SEED_AVAILABLE_CREDIT = 3754.33
SEED_USD_BALANCE = 2847.63
PAYMENT_AMOUNT = 100


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()

    credit = state.get("paypalCredit")
    if not credit:
        return False, "paypalCredit not found in state."

    current_balance = credit.get("currentBalance")
    available_credit = credit.get("availableCredit")
    last_payment = credit.get("lastPaymentAmount")

    errors = []

    # Check current balance decreased
    if current_balance is None:
        errors.append("currentBalance is missing.")
    elif abs(current_balance - (SEED_BALANCE - PAYMENT_AMOUNT)) > 0.01:
        errors.append(
            f"Expected currentBalance around {SEED_BALANCE - PAYMENT_AMOUNT}, got {current_balance}."
        )

    # Check available credit increased
    if available_credit is None:
        errors.append("availableCredit is missing.")
    elif available_credit <= SEED_AVAILABLE_CREDIT:
        errors.append(
            f"Expected availableCredit to increase from {SEED_AVAILABLE_CREDIT}, got {available_credit}."
        )

    # Check last payment amount
    if last_payment is None:
        errors.append("lastPaymentAmount is missing.")
    elif last_payment != PAYMENT_AMOUNT:
        errors.append(
            f"Expected lastPaymentAmount to be {PAYMENT_AMOUNT}, got {last_payment}."
        )

    # Check USD balance decreased
    balances = state.get("balances", [])
    usd_balance = None
    for b in balances:
        if b.get("currency") == "USD":
            usd_balance = b.get("amount")
            break
    if usd_balance is None:
        # Try top-level balance
        usd_balance = state.get("balance", {}).get("amount") if isinstance(state.get("balance"), dict) else state.get("balance")

    if usd_balance is not None:
        if usd_balance >= SEED_USD_BALANCE:
            errors.append(
                f"Expected USD balance to decrease from {SEED_USD_BALANCE}, got {usd_balance}."
            )
    else:
        errors.append("Could not find USD balance in state.")

    if errors:
        return False, " ".join(errors)
    return True, "Successfully made $100 PayPal Credit payment. Balance decreased, available credit increased, and last payment recorded."
