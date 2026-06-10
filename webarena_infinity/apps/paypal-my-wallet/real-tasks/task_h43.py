import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()

    errors = []

    # The only partially-used gift card is Starbucks with $12.50 remaining.
    # Agent should deposit exactly $12.50 into savings.
    savings = state.get("savingsAccount")
    if savings is None:
        errors.append("Savings account not found.")
    else:
        expected_savings = 12450.82 + 12.50
        if abs(savings.get("balance", 0) - expected_savings) > 0.10:
            errors.append(
                f"Savings balance is {savings.get('balance')}, expected ~{expected_savings} "
                f"after depositing $12.50."
            )

        # Check for a deposit of $12.50 in transfer history
        transfers = savings.get("transferHistory", [])
        seed_tx_ids = {"stx_001", "stx_002", "stx_003", "stx_004",
                       "stx_005", "stx_006", "stx_007", "stx_008"}
        found_deposit = False
        for tx in transfers:
            if (tx.get("type") == "deposit"
                    and tx.get("id") not in seed_tx_ids
                    and abs(tx.get("amount", 0) - 12.50) < 0.10):
                found_deposit = True
                break
        if not found_deposit:
            errors.append("No new savings deposit of ~$12.50 found in transfer history.")

    # USD balance should have decreased by $12.50
    balances = state.get("balances", [])
    usd_bal = None
    for b in balances:
        if b.get("currency") == "USD":
            usd_bal = b
            break

    if usd_bal is None:
        errors.append("USD balance not found.")
    else:
        expected_usd = 2847.63 - 12.50
        if abs(usd_bal.get("amount", 0) - expected_usd) > 1.0:
            errors.append(
                f"USD balance is {usd_bal.get('amount')}, expected ~{expected_usd}."
            )

    if errors:
        return False, " ".join(errors)
    return True, "Deposited partially-used gift card remaining balance ($12.50) into savings."
