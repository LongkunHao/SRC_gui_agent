import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()

    errors = []

    # Check rewards.totalPoints decreased from 4825 by 500
    rewards = state.get("rewards")
    if rewards is None:
        return False, "No rewards found in state."

    total_points = rewards.get("totalPoints")
    expected_points = 4325  # 4825 - 500
    if total_points is None:
        errors.append("rewards.totalPoints is missing.")
    elif total_points != expected_points:
        errors.append(
            f"rewards.totalPoints is {total_points}, expected {expected_points} "
            f"(original 4825 minus 500 redeemed)."
        )

    # Check USD balance increased by $5 (500 pts / 100 = $5)
    balances = state.get("balances", [])
    usd_balance = None
    for bal in balances:
        if bal.get("currency") == "USD":
            usd_balance = bal.get("amount")
            break

    if usd_balance is None:
        errors.append("USD balance not found in state.")
    else:
        expected_usd = 2852.63  # 2847.63 + 5.00
        if abs(usd_balance - expected_usd) > 0.02:
            errors.append(
                f"USD balance is {usd_balance}, expected ~{expected_usd} "
                f"(original 2847.63 plus $5 from 500 points redeemed)."
            )

    # Check rewards.history has new entry with type "redeemed" and description containing "PayPal Balance"
    history = rewards.get("history", [])
    found_redemption = False
    for entry in history:
        if entry.get("type") == "redeemed":
            desc = (entry.get("description") or "").lower()
            if "paypal balance" in desc:
                points = entry.get("points", 0)
                if points == -500 or abs(points) == 500:
                    found_redemption = True
                    break

    if not found_redemption:
        errors.append(
            "No redemption entry found in rewards.history with type 'redeemed', "
            "500 points, and description containing 'PayPal Balance'."
        )

    if errors:
        return False, " ".join(errors)
    return True, "Successfully redeemed 500 reward points for $5 PayPal balance."
