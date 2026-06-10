import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()

    errors = []

    # Check HKD balance exists and has positive amount
    balances = state.get("balances", [])
    hkd_bal = None
    for b in balances:
        if b.get("currency") == "HKD":
            hkd_bal = b
            break

    if hkd_bal is None:
        errors.append("Hong Kong Dollar (HKD) not found in balances.")
    elif hkd_bal.get("amount", 0) <= 0:
        errors.append(
            f"HKD balance is {hkd_bal.get('amount')}, expected > 0 after converting $250."
        )

    # Check for currency_convert transaction
    transactions = state.get("transactions", [])
    found_convert = False
    for t in transactions:
        if t.get("type") == "currency_convert":
            desc = (t.get("description") or "").upper()
            if "HKD" in desc:
                found_convert = True
                break
    if not found_convert:
        errors.append("No currency_convert transaction to HKD found.")

    # Check debit card ATM limit is 200
    debit = state.get("paypalDebitCard")
    if debit is None:
        errors.append("PayPal Debit Card not found.")
    elif debit.get("dailyATMLimit") != 200:
        errors.append(
            f"Daily ATM limit is {debit.get('dailyATMLimit')}, expected 200."
        )

    if errors:
        return False, " ".join(errors)
    return True, "Added HKD, converted $250 into it, and set ATM limit to $200."
