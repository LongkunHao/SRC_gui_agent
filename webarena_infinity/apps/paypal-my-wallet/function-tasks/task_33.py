import requests


SEED_BALANCE = 1245.67
SEED_USD_BALANCE = 2847.63
MINIMUM_PAYMENT = 35


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()

    credit = state.get("paypalCredit")
    if not credit:
        return False, "paypalCredit not found in state."

    current_balance = credit.get("currentBalance")
    last_payment = credit.get("lastPaymentAmount")

    errors = []

    # Check current balance decreased
    if current_balance is None:
        errors.append("currentBalance is missing.")
    elif abs(current_balance - (SEED_BALANCE - MINIMUM_PAYMENT)) > 0.01:
        errors.append(
            f"Expected currentBalance around {SEED_BALANCE - MINIMUM_PAYMENT}, got {current_balance}."
        )

    # Check last payment amount
    if last_payment is None:
        errors.append("lastPaymentAmount is missing.")
    elif last_payment != MINIMUM_PAYMENT:
        errors.append(
            f"Expected lastPaymentAmount to be {MINIMUM_PAYMENT}, got {last_payment}."
        )

    # Check USD balance decreased
    balances = state.get("balances", [])
    usd_balance = None
    for b in balances:
        if b.get("currency") == "USD":
            usd_balance = b.get("amount")
            break
    if usd_balance is None:
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
    return True, "Successfully made minimum payment of $35. Balance decreased and last payment recorded."
