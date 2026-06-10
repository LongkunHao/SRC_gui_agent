import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()

    errors = []

    gift_cards = state.get("giftCards", [])
    user_email = "jordan.mitchell@outlook.com"

    # Check for new Starbucks $25 gift card (self)
    # Seed already has gc_002 Starbucks $25 (partially_used), so look for a NEW one
    starbucks_found = False
    for gc in gift_cards:
        if (gc.get("merchantName", "").lower() == "starbucks"
                and gc.get("amount") == 25
                and gc.get("status") == "active"
                and gc.get("id") != "gc_002"):
            if gc.get("recipientEmail") != user_email:
                errors.append(
                    f"New Starbucks gift card recipient is '{gc.get('recipientEmail')}', "
                    f"expected '{user_email}' (self-purchase)."
                )
            starbucks_found = True
            break

    if not starbucks_found:
        errors.append("No new active Starbucks $25 gift card found.")

    # Check for new Nike $50 gift card (self)
    nike_found = False
    for gc in gift_cards:
        if (gc.get("merchantName", "").lower() == "nike"
                and gc.get("amount") == 50
                and gc.get("status") == "active"):
            if gc.get("recipientEmail") != user_email:
                errors.append(
                    f"Nike gift card recipient is '{gc.get('recipientEmail')}', "
                    f"expected '{user_email}' (self-purchase)."
                )
            nike_found = True
            break

    if not nike_found:
        errors.append("No active Nike $50 gift card found.")

    # USD balance should decrease by $75 (25 + 50)
    balances = state.get("balances", [])
    usd_bal = None
    for b in balances:
        if b.get("currency") == "USD":
            usd_bal = b
            break

    if usd_bal is None:
        errors.append("USD balance not found.")
    else:
        expected_usd = round(2847.63 - 75, 2)
        if abs(usd_bal.get("amount", 0) - expected_usd) > 5.0:
            errors.append(
                f"USD balance is {usd_bal.get('amount')}, expected ~{expected_usd} "
                f"after two gift card purchases totaling $75."
            )

    if errors:
        return False, " ".join(errors)
    return True, "Successfully purchased $25 Starbucks and $50 Nike gift cards for self."
