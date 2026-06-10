import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()

    errors = []

    rewards = state.get("rewards")
    if rewards is None:
        errors.append("No rewards found in state.")
    else:
        # Check totalPoints decreased from 4825 by 1000
        total_points = rewards.get("totalPoints")
        if total_points is None:
            errors.append("rewards.totalPoints is missing.")
        elif total_points != 3825:
            errors.append(
                f"rewards.totalPoints is {total_points}, expected 3825 "
                f"(original 4825 minus 1000)."
            )

        # Check for new redeemed entry containing "Gift Card"
        history = rewards.get("history", [])
        found_redemption = False
        for entry in history:
            if (entry.get("type") == "redeemed" and
                    "Gift Card" in entry.get("description", "")):
                found_redemption = True
                break

        if not found_redemption:
            errors.append(
                "No rewards history entry with type 'redeemed' and description "
                "containing 'Gift Card' found."
            )

    if errors:
        return False, " ".join(errors)
    return True, "Successfully redeemed 1,000 rewards points for a gift card: totalPoints is 3825 and redemption recorded in history."
