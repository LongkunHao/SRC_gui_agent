import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()

    errors = []

    # Check USD balance increased from 2847.63 by 200
    balances = state.get("balances", [])
    usd_balance = None
    for bal in balances:
        if bal.get("currency") == "USD":
            usd_balance = bal.get("amount")
            break

    if usd_balance is None:
        errors.append("USD balance not found in state.")
    else:
        expected_usd = 3047.63  # 2847.63 + 200
        if abs(usd_balance - expected_usd) > 0.02:
            errors.append(
                f"USD balance is {usd_balance}, expected ~{expected_usd} "
                f"(original 2847.63 plus 200 transfer in)."
            )

    # Check for a transfer_in transaction containing "Bank of America" in description
    transactions = state.get("transactions", [])
    found_transfer = False
    for txn in transactions:
        if txn.get("type") == "transfer_in":
            desc = (txn.get("description") or "").lower()
            if "bank of america" in desc:
                amount = txn.get("amount", 0)
                if abs(amount) >= 199 and abs(amount) <= 201:
                    found_transfer = True
                    break

    if not found_transfer:
        errors.append(
            "No transfer_in transaction found with 'Bank of America' in the description "
            "and amount of ~$200."
        )

    if errors:
        return False, " ".join(errors)
    return True, "Successfully loaded $200 into PayPal from Bank of America."
