import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()

    errors = []

    bank_accounts = state.get("bankAccounts", [])

    # Savings-type bank accounts should be removed:
    # Bank of America 3891 (savings) and US Bank 7823 (savings)
    remaining_last_fours = {b.get("lastFour") for b in bank_accounts}

    for lf in ["3891", "7823"]:
        if lf in remaining_last_fours:
            errors.append(f"Savings-type bank account ending in {lf} should have been removed.")

    # Checking accounts should remain: Chase 6742, Wells Fargo 5518, Citibank 1104
    for lf in ["6742", "5518", "1104"]:
        if lf not in remaining_last_fours:
            errors.append(f"Checking account ending in {lf} was removed but should have been kept.")

    # Savings account should have decreased by $500 (from 12450.82 to ~11950.82)
    savings = state.get("savingsAccount")
    if savings is None:
        errors.append("PayPal Savings account not found.")
    else:
        expected_savings = 12450.82 - 500
        if abs(savings.get("balance", 0) - expected_savings) > 1.0:
            errors.append(
                f"Savings balance is {savings.get('balance')}, expected ~{expected_savings} "
                f"after withdrawing $500."
            )

    if errors:
        return False, " ".join(errors)
    return True, "Removed all savings-type bank accounts and withdrew $500 from PayPal Savings."
