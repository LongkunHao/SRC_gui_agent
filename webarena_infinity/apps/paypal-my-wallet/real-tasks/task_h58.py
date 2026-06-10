import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()

    errors = []

    # Rewards earned this year = 2150 (seed). 10% = 215 points to redeem.
    rewards = state.get("rewards")
    if rewards is None:
        return False, "Rewards not found."

    expected_points = 4825 - 215
    if rewards.get("totalPoints") != expected_points:
        errors.append(
            f"Rewards points is {rewards.get('totalPoints')}, expected {expected_points} "
            f"(seed 4825 minus 215 redeemed)."
        )

    # Check for redemption in history
    history = rewards.get("history", [])
    seed_rwd_ids = {f"rwd_{i:03d}" for i in range(1, 13)}
    found_redeem = False
    for h in history:
        if (h.get("type") == "redeemed"
                and h.get("id") not in seed_rwd_ids
                and h.get("points") == -215):
            found_redeem = True
            break
    if not found_redeem:
        errors.append("No redemption of 215 points found in rewards history.")

    # USD balance should have increased by $2.15 (215 points * $0.01)
    balances = state.get("balances", [])
    usd_bal = None
    for b in balances:
        if b.get("currency") == "USD":
            usd_bal = b
            break

    if usd_bal is None:
        errors.append("USD balance not found.")
    else:
        expected_usd = 2847.63 + 2.15
        if abs(usd_bal.get("amount", 0) - expected_usd) > 0.50:
            errors.append(
                f"USD balance is {usd_bal.get('amount')}, expected ~{expected_usd}."
            )

    if errors:
        return False, " ".join(errors)
    return True, "Redeemed 215 reward points (10% of 2150 earned this year) for PayPal balance."
