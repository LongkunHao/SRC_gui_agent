import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()

    prefs = state.get("walletPreferences", {})
    notifications = prefs.get("emailNotifications", {})
    promotions = notifications.get("promotions")

    if promotions is not True:
        return False, f"Expected walletPreferences.emailNotifications.promotions to be True, got {promotions}."

    return True, "Promotions notifications have been successfully enabled."
