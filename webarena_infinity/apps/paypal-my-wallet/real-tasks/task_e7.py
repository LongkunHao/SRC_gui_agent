import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()

    prefs = state.get("walletPreferences")
    if prefs is None:
        return False, "No wallet preferences found in state."

    email_notifs = prefs.get("emailNotifications")
    if email_notifs is None:
        return False, "No email notification preferences found in state."

    if email_notifs.get("promotions") is not True:
        return False, f"Promotional emails are not enabled (promotions={email_notifs.get('promotions')})."

    return True, "Promotional email notifications have been successfully enabled."
