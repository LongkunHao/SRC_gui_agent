import requests


SEED_TOTAL_POINTS = 4825
SEED_USD_BALANCE = 2847.63
REDEEMED_POINTS = 1000


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

    # Check rewards history for gift card redemption entry
    history = rewards.get("history", [])
    found_redemption = False
    for entry in history:
        points = entry.get("points", 0)
        entry_type = entry.get("type", "")
        description = entry.get("description", "")
        if points == -REDEEMED_POINTS and entry_type == "redeemed" and "Gift Card" in description:
            found_redemption = True
            break

    if not found_redemption:
        errors.append(
            f"No rewards history entry found with points==-{REDEEMED_POINTS}, type=='redeemed', and description containing 'Gift Card'."
        )

    # Check USD balance did NOT increase (gift card redemption shouldn't affect balance)
    balances = state.get("balances", [])
    usd_balance = None
    for b in balances:
        if b.get("currency") == "USD":
            usd_balance = b.get("amount")
            break
    if usd_balance is None:
        usd_balance = state.get("balance", {}).get("amount") if isinstance(state.get("balance"), dict) else state.get("balance")

    if usd_balance is not None:
        if usd_balance > SEED_USD_BALANCE + 0.01:
            errors.append(
                f"USD balance should NOT have increased for gift card redemption. Expected <= {SEED_USD_BALANCE}, got {usd_balance}."
            )
    else:
        errors.append("Could not find USD balance in state.")

    if errors:
        return False, " ".join(errors)
    return True, "Successfully redeemed 1000 points for a gift card. Points decreased to 3825 and USD balance was not affected."
