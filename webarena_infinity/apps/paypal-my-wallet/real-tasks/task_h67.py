import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()

    errors = []

    # Savings interest earned this month is $43.62 (seed).
    # Should redeem 4362 points worth $43.62 as PayPal Balance.
    # Seed total points: 4825. After: 4825 - 4362 = 463.

    rewards = state.get("rewards", {})
    expected_points = 4825 - 4362
    actual_points = rewards.get("totalPoints", 0)
    if abs(actual_points - expected_points) > 5:
        errors.append(
            f"Reward points are {actual_points}, expected ~{expected_points} "
            f"after redeeming 4362 points ($43.62 = savings interest this month)."
        )

    # Check for a redemption entry in rewards history
    history = rewards.get("history", [])
    found_redeem = any(
        h.get("type") == "redeemed" and h.get("points", 0) == -4362
        for h in history
    )
    if not found_redeem:
        # Allow some flexibility — check for approximate redemption
        found_redeem_approx = any(
            h.get("type") == "redeemed" and abs(h.get("points", 0) + 4362) <= 5
            for h in history
        )
        if not found_redeem_approx:
            errors.append("No redemption of ~4362 points found in rewards history.")

    # USD balance should have increased by ~$43.62
    balances = state.get("balances", [])
    usd = None
    for b in balances:
        if b.get("currency") == "USD":
            usd = b
            break

    if usd is None:
        errors.append("USD balance not found.")
    else:
        expected_usd = 2847.63 + 43.62
        if abs(usd.get("amount", 0) - expected_usd) > 1.0:
            errors.append(
                f"USD balance is {usd.get('amount')}, expected ~{expected_usd} "
                f"after redeeming $43.62 in rewards."
            )

    if errors:
        return False, " ".join(errors)
    return True, "Redeemed savings interest amount ($43.62 = 4362 points) as PayPal Balance."
