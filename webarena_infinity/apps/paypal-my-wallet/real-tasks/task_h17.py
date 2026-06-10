import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()

    errors = []

    # Check for new Starbucks gift card with amount 25, self-purchase, active
    gift_cards = state.get("giftCards", [])
    starbucks_gc = None
    for gc in gift_cards:
        if (gc.get("merchantName", "").lower() == "starbucks"
                and gc.get("amount") == 25
                and gc.get("status") == "active"
                and gc.get("recipientEmail") == "jordan.mitchell@outlook.com"):
            starbucks_gc = gc
            break

    if starbucks_gc is None:
        # Try to find any new Starbucks card with amount 25
        found_any = False
        for gc in gift_cards:
            if gc.get("merchantName", "").lower() == "starbucks" and gc.get("amount") == 25:
                found_any = True
                if gc.get("status") != "active":
                    errors.append(
                        f"Found Starbucks $25 gift card but status is '{gc.get('status')}', expected 'active'."
                    )
                if gc.get("recipientEmail") != "jordan.mitchell@outlook.com":
                    errors.append(
                        f"Found Starbucks $25 gift card but recipientEmail is '{gc.get('recipientEmail')}', "
                        f"expected 'jordan.mitchell@outlook.com' (self-purchase)."
                    )
                break
        if not found_any:
            errors.append(
                "No new Starbucks gift card with amount $25 found in giftCards."
            )

    # Check rewards totalPoints decreased from 4825 by 500
    rewards = state.get("rewards")
    if rewards is None:
        errors.append("No rewards found in state.")
    else:
        total_points = rewards.get("totalPoints")
        expected_points = 4325  # 4825 - 500
        if total_points is None:
            errors.append("rewards.totalPoints is missing.")
        elif total_points != expected_points:
            errors.append(
                f"rewards.totalPoints is {total_points}, expected {expected_points} "
                f"(original 4825 minus 500 redeemed)."
            )

        # Check rewards history has a redeemed entry for "PayPal Balance"
        history = rewards.get("history", [])
        found_redemption = False
        for entry in history:
            if entry.get("type") == "redeemed":
                desc = (entry.get("description") or "").lower()
                if "paypal balance" in desc or "paypal" in desc:
                    found_redemption = True
                    break
        if not found_redemption:
            errors.append(
                "No redeemed entry for 'PayPal Balance' found in rewards.history."
            )

    # Check USD balance: 2847.63 - 25 (gift card) + 5 (500 pts redemption) = 2827.63
    balances = state.get("balances", [])
    usd_balance = None
    for bal in balances:
        if bal.get("currency") == "USD":
            usd_balance = bal.get("amount")
            break

    if usd_balance is None:
        errors.append("USD balance not found in state.")
    else:
        expected_usd = 2827.63  # 2847.63 - 25 + 5
        if abs(usd_balance - expected_usd) > 1.0:
            errors.append(
                f"USD balance is {usd_balance}, expected ~{expected_usd} "
                f"(original 2847.63 minus 25 gift card plus 5 rewards redemption)."
            )

    if errors:
        return False, " ".join(errors)
    return True, "Successfully purchased $25 Starbucks gift card and redeemed 500 rewards points for PayPal balance."
