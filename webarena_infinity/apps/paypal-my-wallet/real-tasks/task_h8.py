import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()

    errors = []

    # Check savings account balance decreased by 2000 from 12450.82
    savings = state.get("savingsAccount")
    if savings is None:
        errors.append("No savingsAccount found in state.")
    else:
        expected_savings = round(12450.82 - 2000, 2)  # 10450.82
        actual_savings = savings.get("balance", 0)
        if abs(actual_savings - expected_savings) > 1.0:
            errors.append(
                f"savingsAccount.balance is {actual_savings}, expected approximately {expected_savings} "
                f"(seed 12450.82 minus 2000)."
            )

        # Check savings transferHistory has a withdrawal entry
        transfer_history = savings.get("transferHistory", [])
        has_withdrawal = False
        for entry in transfer_history:
            if entry.get("type") == "withdrawal" and entry.get("amount") == 2000:
                has_withdrawal = True
                break
        # Also accept approximate amounts
        if not has_withdrawal:
            for entry in transfer_history:
                if entry.get("type") == "withdrawal":
                    amt = entry.get("amount", 0)
                    if abs(amt - 2000) < 1.0:
                        has_withdrawal = True
                        break
        if not has_withdrawal:
            # Check if there's any new withdrawal (beyond the 2 seed withdrawals stx_003, stx_006)
            seed_withdrawal_ids = {"stx_003", "stx_006"}
            for entry in transfer_history:
                if entry.get("type") == "withdrawal" and entry.get("id") not in seed_withdrawal_ids:
                    has_withdrawal = True
                    break
        if not has_withdrawal:
            errors.append("No withdrawal entry found in savingsAccount.transferHistory for the $2,000 transfer.")

    # Check USD balance: seed was 2847.63, +2000 from savings, -1000 to Chase = 3847.63
    balances = state.get("balances", [])
    usd_bal = None
    for b in balances:
        if b.get("currency") == "USD":
            usd_bal = b
            break

    if usd_bal is None:
        errors.append("USD balance not found.")
    else:
        expected_usd = round(2847.63 + 2000 - 1000, 2)  # 3847.63
        actual_usd = usd_bal.get("amount", 0)
        if abs(actual_usd - expected_usd) > 5.0:
            errors.append(
                f"USD balance is {actual_usd}, expected approximately {expected_usd} "
                f"(seed 2847.63 + 2000 from savings - 1000 to Chase)."
            )

    # Check for transfer_out transaction to Chase
    transactions = state.get("transactions", [])
    chase_txn = None
    for t in transactions:
        if t.get("type") == "transfer_out":
            desc = t.get("description", "").lower()
            if "chase" in desc and t.get("id") != "txn_005":
                chase_txn = t
                break

    if chase_txn is None:
        errors.append("No new transfer_out transaction containing 'Chase' found.")

    if errors:
        return False, " ".join(errors)
    return True, "Successfully moved $2,000 from savings to main balance and withdrew $1,000 to Chase."
