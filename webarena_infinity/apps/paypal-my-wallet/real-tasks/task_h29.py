import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()

    errors = []

    prefs = state.get("walletPreferences")
    if prefs is None:
        return False, "No walletPreferences found."

    notifs = prefs.get("emailNotifications")
    if notifs is None:
        return False, "No emailNotifications found."

    # Payments should be OFF (was True)
    if notifs.get("payments") is not False:
        errors.append(
            f"payments notification is {notifs.get('payments')}, expected False."
        )

    # Transfers should be OFF (was True)
    if notifs.get("transfers") is not False:
        errors.append(
            f"transfers notification is {notifs.get('transfers')}, expected False."
        )

    # Promotions should be ON (was False)
    if notifs.get("promotions") is not True:
        errors.append(
            f"promotions notification is {notifs.get('promotions')}, expected True."
        )

    # Other notifications should remain unchanged from seed
    if notifs.get("securityAlerts") is not True:
        errors.append(f"securityAlerts changed unexpectedly to {notifs.get('securityAlerts')}.")
    if notifs.get("cryptoAlerts") is not True:
        errors.append(f"cryptoAlerts changed unexpectedly to {notifs.get('cryptoAlerts')}.")
    if notifs.get("rewardsUpdates") is not True:
        errors.append(f"rewardsUpdates changed unexpectedly to {notifs.get('rewardsUpdates')}.")
    if notifs.get("weeklyDigest") is not True:
        errors.append(f"weeklyDigest changed unexpectedly to {notifs.get('weeklyDigest')}.")

    if errors:
        return False, " ".join(errors)
    return True, "Payment and transfer notifications off, promotions on, others unchanged."
