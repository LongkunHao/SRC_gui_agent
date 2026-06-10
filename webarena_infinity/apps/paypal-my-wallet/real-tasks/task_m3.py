import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()

    errors = []

    # Check USD balance decreased from 2847.63 by 300
    balances = state.get("balances", [])
    usd_balance = None
    for bal in balances:
        if bal.get("currency") == "USD":
            usd_balance = bal.get("amount")
            break

    if usd_balance is None:
        errors.append("USD balance not found in state.")
    else:
        expected_usd = 2547.63  # 2847.63 - 300
        if abs(usd_balance - expected_usd) > 0.02:
            errors.append(
                f"USD balance is {usd_balance}, expected ~{expected_usd} "
                f"(original 2847.63 minus 300 transfer)."
            )

    # Check for a transfer_out transaction containing "Chase" in description
    transactions = state.get("transactions", [])
    found_transfer = False
    for txn in transactions:
        if txn.get("type") == "transfer_out":
            desc = (txn.get("description") or "").lower()
            if "chase" in desc:
                amount = txn.get("amount", 0)
                if abs(amount) >= 299 and abs(amount) <= 301:
                    found_transfer = True
                    break

    if not found_transfer:
        errors.append(
            "No transfer_out transaction found with 'Chase' in the description "
            "and amount of ~$300."
        )

    if errors:
        return False, " ".join(errors)
    return True, "Successfully sent $300 from PayPal balance to Chase checking."
