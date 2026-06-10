import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()

    errors = []

    prefs = state.get("walletPreferences")
    if prefs is None:
        return False, "No walletPreferences found in state."

    email_notifs = prefs.get("emailNotifications")
    if email_notifs is None:
        return False, "No emailNotifications found in walletPreferences."

    # Only payments, transfers, and securityAlerts should be True.
    expected = {
        "payments": True,
        "transfers": True,
        "securityAlerts": True,
        "promotions": False,
        "cryptoAlerts": False,
        "rewardsUpdates": False,
        "weeklyDigest": False,
    }

    for key, expected_val in expected.items():
        actual_val = email_notifs.get(key)
        if actual_val is not expected_val:
            errors.append(
                f"emailNotifications.{key} is {actual_val}, expected {expected_val}."
            )

    if errors:
        return False, " ".join(errors)
    return True, "Email notifications set to payments, transfers, and security alerts only."
