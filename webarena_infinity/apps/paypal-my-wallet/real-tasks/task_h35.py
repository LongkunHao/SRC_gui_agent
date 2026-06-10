import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()

    errors = []

    # Rewards points should decrease by 2000 (from 4825 to 2825)
    rewards = state.get("rewards")
    if rewards is None:
        errors.append("No rewards found in state.")
    else:
        expected_points = 2825
        actual_points = rewards.get("totalPoints", 0)
        if actual_points != expected_points:
            errors.append(
                f"Rewards totalPoints is {actual_points}, expected {expected_points} "
                f"(original 4825 minus 2000 redeemed)."
            )

        # Check for redemption in history
        history = rewards.get("history", [])
        found_redemption = False
        for entry in history:
            if entry.get("type") == "redeemed":
                desc = (entry.get("description") or "").lower()
                if "paypal balance" in desc or "balance" in desc:
                    found_redemption = True
                    break
        if not found_redemption:
            errors.append("No redemption for PayPal Balance found in rewards history.")

    # Savings should increase by ~$20 (from 12450.82)
    savings = state.get("savingsAccount")
    if savings is None:
        errors.append("No savingsAccount found.")
    else:
        expected_savings = round(12450.82 + 20, 2)
        actual_savings = savings.get("balance", 0)
        if abs(actual_savings - expected_savings) > 2.0:
            errors.append(
                f"Savings balance is {actual_savings}, expected ~{expected_savings} "
                f"after depositing $20."
            )

    if errors:
        return False, " ".join(errors)
    return True, "Redeemed 2,000 reward points for balance and deposited $20 into savings."
