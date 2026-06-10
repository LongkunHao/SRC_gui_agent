import requests


SEED_TOTAL_POINTS = 4825
SEED_USD_BALANCE = 2847.63
REDEEMED_POINTS = 500
POINTS_VALUE = 5.00  # 500 pts / 100 = $5.00


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()

    rewards = state.get("rewards")
    if not rewards:
        return False, "rewards not found in state."

    errors = []

    # Check total points decreased
    total_points = rewards.get("totalPoints")
    expected_points = SEED_TOTAL_POINTS - REDEEMED_POINTS
    if total_points is None:
        errors.append("totalPoints is missing.")
    elif total_points != expected_points:
        errors.append(
            f"Expected totalPoints to be {expected_points}, got {total_points}."
        )

    # Check rewards history for redemption entry
    history = rewards.get("history", [])
    found_redemption = False
    for entry in history:
        points = entry.get("points", 0)
        entry_type = entry.get("type", "")
        description = entry.get("description", "")
        if points == -REDEEMED_POINTS and entry_type == "redeemed" and "PayPal Balance" in description:
            found_redemption = True
            break

    if not found_redemption:
        errors.append(
            f"No rewards history entry found with points==-{REDEEMED_POINTS}, type=='redeemed', and description containing 'PayPal Balance'."
        )

    # Check USD balance increased by $5.00
    balances = state.get("balances", [])
    usd_balance = None
    for b in balances:
        if b.get("currency") == "USD":
            usd_balance = b.get("amount")
            break
    if usd_balance is None:
        usd_balance = state.get("balance", {}).get("amount") if isinstance(state.get("balance"), dict) else state.get("balance")

    if usd_balance is not None:
        expected_usd = SEED_USD_BALANCE + POINTS_VALUE
        if abs(usd_balance - expected_usd) > 0.01:
            errors.append(
                f"Expected USD balance around {expected_usd}, got {usd_balance}."
            )
    else:
        errors.append("Could not find USD balance in state.")

    if errors:
        return False, " ".join(errors)
    return True, "Successfully redeemed 500 points for PayPal Balance. Points decreased to 4325 and USD balance increased by $5.00."
