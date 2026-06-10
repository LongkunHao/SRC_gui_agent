import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()

    prefs = state.get("walletPreferences", {})
    notifications = prefs.get("emailNotifications", {})
    weekly_digest = notifications.get("weeklyDigest")

    if weekly_digest is not False:
        return False, f"Expected walletPreferences.emailNotifications.weeklyDigest to be False, got {weekly_digest}."

    return True, "Weekly digest has been successfully disabled."
