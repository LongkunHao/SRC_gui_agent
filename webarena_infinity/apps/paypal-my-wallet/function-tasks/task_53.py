import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()

    prefs = state.get("walletPreferences", {})
    notifications = prefs.get("emailNotifications", {})
    rewards_updates = notifications.get("rewardsUpdates")

    if rewards_updates is not False:
        return False, f"Expected walletPreferences.emailNotifications.rewardsUpdates to be False, got {rewards_updates}."

    return True, "Rewards updates have been successfully disabled."
