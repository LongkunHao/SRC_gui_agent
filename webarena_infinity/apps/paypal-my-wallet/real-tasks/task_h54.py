import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()

    errors = []

    # Check rewards decreased by 2000 (from 4825 to 2825)
    rewards = state.get("rewards")
    if rewards is None:
        errors.append("Rewards not found.")
    else:
        expected_points = 4825 - 2000
        if rewards.get("totalPoints") != expected_points:
            errors.append(
                f"Rewards points is {rewards.get('totalPoints')}, expected {expected_points}."
            )

        # Check for redemption in history
        history = rewards.get("history", [])
        seed_rwd_ids = {f"rwd_{i:03d}" for i in range(1, 13)}
        found_redeem = False
        for h in history:
            if (h.get("type") == "redeemed"
                    and h.get("id") not in seed_rwd_ids
                    and h.get("points") == -2000):
                found_redeem = True
                break
        if not found_redeem:
            errors.append("No redemption of 2000 points found in rewards history.")

    # Check SOL quantity > 0 (was 0 in seed)
    crypto_holdings = state.get("cryptoHoldings", [])
    sol = None
    for c in crypto_holdings:
        if c.get("symbol") == "SOL":
            sol = c
            break

    if sol is None:
        errors.append("Solana not found in crypto holdings.")
    else:
        if sol.get("quantity", 0) <= 0:
            errors.append(
                f"Solana quantity is {sol.get('quantity')}, expected > 0 "
                f"after buying $10 worth."
            )

    if errors:
        return False, " ".join(errors)
    return True, "Redeemed 2000 reward points for balance and bought $10 of Solana."
