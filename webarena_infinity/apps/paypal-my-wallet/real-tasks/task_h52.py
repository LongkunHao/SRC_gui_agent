import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()

    errors = []

    # Active gift cards by remaining balance:
    #   Home Depot: $75.00 (highest)
    #   Amazon: $50.00
    #   Netflix: $30.00
    #   Starbucks: $12.50 (partially_used)
    # Agent should buy a $25 Home Depot gift card for themselves.
    gift_cards = state.get("giftCards", [])
    seed_gc_ids = {"gc_001", "gc_002", "gc_003", "gc_004", "gc_005"}
    found_gc = False
    for gc in gift_cards:
        if gc.get("id") not in seed_gc_ids:
            if (gc.get("merchantName") == "Home Depot"
                    and gc.get("amount") == 25):
                # Verify it's for self
                user = state.get("currentUser", {})
                user_email = user.get("email", "")
                if gc.get("recipientEmail") == user_email:
                    found_gc = True
                    break
    if not found_gc:
        errors.append(
            "No new $25 Home Depot gift card for self found. "
            "Home Depot has the highest active gift card balance ($75)."
        )

    # USD balance should have decreased by $25
    balances = state.get("balances", [])
    usd_bal = None
    for b in balances:
        if b.get("currency") == "USD":
            usd_bal = b
            break

    if usd_bal is None:
        errors.append("USD balance not found.")
    else:
        expected_usd = 2847.63 - 25
        if abs(usd_bal.get("amount", 0) - expected_usd) > 1.0:
            errors.append(
                f"USD balance is {usd_bal.get('amount')}, expected ~{expected_usd}."
            )

    if errors:
        return False, " ".join(errors)
    return True, "Bought $25 Home Depot gift card for self (highest active gift card balance)."
