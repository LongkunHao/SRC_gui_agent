import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()

    errors = []

    notifs = state.get("walletPreferences", {}).get("emailNotifications", {})

    # Seed state:
    # payments: true -> false
    # transfers: true -> false
    # securityAlerts: true -> true (exception: always on)
    # promotions: false -> true
    # cryptoAlerts: true -> false
    # rewardsUpdates: true -> false
    # weeklyDigest: true -> false

    expected = {
        "payments": False,
        "transfers": False,
        "securityAlerts": True,
        "promotions": True,
        "cryptoAlerts": False,
        "rewardsUpdates": False,
        "weeklyDigest": False,
    }

    for key, expected_val in expected.items():
        actual_val = notifs.get(key)
        if actual_val != expected_val:
            errors.append(
                f"Notification '{key}' is {actual_val}, expected {expected_val}."
            )

    if errors:
        return False, " ".join(errors)
    return True, "Flipped all email notifications (except security alerts kept enabled)."
