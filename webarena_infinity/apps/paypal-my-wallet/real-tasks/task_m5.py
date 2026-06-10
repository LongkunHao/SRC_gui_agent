import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()

    errors = []

    # Check savingsAccount.balance increased from 12450.82 by 500
    savings = state.get("savingsAccount")
    if savings is None:
        return False, "No savingsAccount found in state."

    savings_balance = savings.get("balance")
    expected_savings = 12950.82  # 12450.82 + 500
    if savings_balance is None:
        errors.append("savingsAccount.balance is missing.")
    elif abs(savings_balance - expected_savings) > 0.02:
        errors.append(
            f"savingsAccount.balance is {savings_balance}, expected ~{expected_savings} "
            f"(original 12450.82 plus 500 deposit)."
        )

    # Check USD balance decreased from 2847.63 by 500
    balances = state.get("balances", [])
    usd_balance = None
    for bal in balances:
        if bal.get("currency") == "USD":
            usd_balance = bal.get("amount")
            break

    if usd_balance is None:
        errors.append("USD balance not found in state.")
    else:
        expected_usd = 2347.63  # 2847.63 - 500
        if abs(usd_balance - expected_usd) > 0.02:
            errors.append(
                f"USD balance is {usd_balance}, expected ~{expected_usd} "
                f"(original 2847.63 minus 500 savings deposit)."
            )

    # Check savings transferHistory has a new deposit entry for 500
    transfer_history = savings.get("transferHistory", [])
    found_deposit = False
    for entry in transfer_history:
        if entry.get("type") == "deposit" and abs(entry.get("amount", 0) - 500) < 0.02:
            found_deposit = True
            break

    if not found_deposit:
        errors.append(
            "No deposit entry of $500 found in savingsAccount.transferHistory."
        )

    if errors:
        return False, " ".join(errors)
    return True, "Successfully moved $500 from main balance into savings."
