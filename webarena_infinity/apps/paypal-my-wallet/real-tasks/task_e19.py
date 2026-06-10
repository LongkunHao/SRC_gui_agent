import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()

    wallet_prefs = state.get("walletPreferences")
    if wallet_prefs is None:
        return False, "walletPreferences not found in state."

    email_notifs = wallet_prefs.get("emailNotifications")
    if email_notifs is None:
        return False, "emailNotifications not found in walletPreferences."

    if email_notifs.get("transfers") is not False:
        return False, f"Transfer email notifications are still enabled (transfers={email_notifs.get('transfers')})."

    return True, "Transfer notification emails have been turned off."
