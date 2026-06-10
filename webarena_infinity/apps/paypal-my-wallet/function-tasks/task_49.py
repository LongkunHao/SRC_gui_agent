import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()

    prefs = state.get("walletPreferences", {})
    notifications = prefs.get("emailNotifications", {})
    payments = notifications.get("payments")

    if payments is not False:
        return False, f"Expected walletPreferences.emailNotifications.payments to be False, got {payments}."

    return True, "Payment notifications have been successfully disabled."
