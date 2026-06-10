import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()

    prefs = state.get("walletPreferences", {})
    notifications = prefs.get("emailNotifications", {})
    crypto_alerts = notifications.get("cryptoAlerts")

    if crypto_alerts is not False:
        return False, f"Expected walletPreferences.emailNotifications.cryptoAlerts to be False, got {crypto_alerts}."

    return True, "Crypto alerts have been successfully disabled."
