import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()

    errors = []

    # USD balance should decrease by $500 (withdrawal to BofA)
    balances = state.get("balances", [])
    usd_bal = None
    for b in balances:
        if b.get("currency") == "USD":
            usd_bal = b
            break

    if usd_bal is None:
        errors.append("USD balance not found.")
    else:
        expected_usd = round(2847.63 - 500, 2)
        if abs(usd_bal.get("amount", 0) - expected_usd) > 5.0:
            errors.append(
                f"USD balance is {usd_bal.get('amount')}, expected ~{expected_usd} "
                f"after withdrawing $500."
            )

    # Check for transfer_out transaction to Bank of America
    transactions = state.get("transactions", [])
    found_transfer = False
    for t in transactions:
        if t.get("type") == "transfer_out":
            desc = (t.get("description") or "").lower()
            if "bank of america" in desc or "3891" in desc:
                found_transfer = True
                break
    if not found_transfer:
        errors.append("No transfer_out transaction to Bank of America found.")

    # Debit card spending limit should be 4000
    debit = state.get("paypalDebitCard")
    if debit is None:
        errors.append("No paypalDebitCard found.")
    else:
        if debit.get("dailySpendingLimit") != 4000:
            errors.append(
                f"Daily spending limit is {debit.get('dailySpendingLimit')}, expected 4000."
            )

    if errors:
        return False, " ".join(errors)
    return True, "Withdrew $500 to Bank of America and set spending limit to $4,000."
