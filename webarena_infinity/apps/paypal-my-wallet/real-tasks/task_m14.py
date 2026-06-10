import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()

    errors = []

    # Check savings balance decreased from 12450.82 by 1000
    savings = state.get("savingsAccount")
    if savings is None:
        errors.append("No savingsAccount found in state.")
    else:
        savings_balance = savings.get("balance")
        expected_savings = 11450.82
        if savings_balance is None:
            errors.append("savingsAccount.balance is missing.")
        elif abs(savings_balance - expected_savings) > 1.0:
            errors.append(
                f"Savings balance is {savings_balance}, expected approximately {expected_savings} "
                f"(original 12450.82 minus 1000)."
            )

        # Check for new withdrawal entry in transferHistory
        transfer_history = savings.get("transferHistory", [])
        found_withdrawal = False
        for entry in transfer_history:
            if entry.get("type") == "withdrawal" and entry.get("amount") == 1000:
                found_withdrawal = True
                break
            # Also accept 1000.0 or 1000.00
            if entry.get("type") == "withdrawal":
                try:
                    if abs(float(entry.get("amount", 0)) - 1000) < 0.01:
                        found_withdrawal = True
                        break
                except (ValueError, TypeError):
                    pass

        if not found_withdrawal:
            errors.append(
                "No withdrawal entry of $1,000 found in savingsAccount.transferHistory."
            )

    # Check USD balance increased by 1000
    balances = state.get("balances", [])
    usd_balance = None
    for b in balances:
        if b.get("currency") == "USD":
            usd_balance = b.get("amount")
            break

    if usd_balance is None:
        errors.append("No USD balance found in state.")
    else:
        expected_usd = 2847.63 + 1000
        if abs(usd_balance - expected_usd) > 5.0:
            errors.append(
                f"USD balance is {usd_balance}, expected approximately {expected_usd} "
                f"(original 2847.63 plus 1000)."
            )

    if errors:
        return False, " ".join(errors)
    return True, "Successfully withdrew $1,000 from savings: savings balance decreased to ~11450.82, USD balance increased to ~3847.63, and withdrawal recorded in transferHistory."
