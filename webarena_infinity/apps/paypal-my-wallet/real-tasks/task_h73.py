import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()

    errors = []

    balances = state.get("balances", [])

    # Step 1: PLN should exist with positive balance
    pln_bal = None
    for b in balances:
        if b.get("currency") == "PLN":
            pln_bal = b
            break

    if pln_bal is None:
        errors.append("Polish Zloty (PLN) not found in balances.")
    elif pln_bal.get("amount", 0) <= 0:
        errors.append(f"PLN balance is {pln_bal.get('amount')}, expected > 0 after converting $200.")

    # Step 2: Should have a currency_convert transaction to PLN
    transactions = state.get("transactions", [])
    found_convert = any(
        t.get("type") == "currency_convert" and "PLN" in (t.get("description") or "").upper()
        for t in transactions
    )
    if not found_convert:
        errors.append("No currency_convert transaction to PLN found.")

    # Step 3: Savings should have increased by $300 (from 12450.82 to ~12750.82)
    savings = state.get("savingsAccount")
    if savings is None:
        errors.append("Savings account not found.")
    else:
        expected_savings = 12450.82 + 300
        if abs(savings.get("balance", 0) - expected_savings) > 1.0:
            errors.append(
                f"Savings balance is {savings.get('balance')}, expected ~{expected_savings} "
                f"after depositing $300."
            )

    # Step 4: ATM limit should be $500
    debit = state.get("paypalDebitCard", {})
    if debit.get("dailyATMLimit") != 500:
        errors.append(
            f"Debit card ATM limit is {debit.get('dailyATMLimit')}, expected 500."
        )

    if errors:
        return False, " ".join(errors)
    return True, "Added PLN, converted $200, deposited $300 to savings, set ATM limit to $500."
