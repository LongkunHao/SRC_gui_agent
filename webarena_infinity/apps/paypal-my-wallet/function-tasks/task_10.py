import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()

    banks = state.get("bankAccounts", [])

    for bank in banks:
        if bank.get("lastFour") == "6742":
            return False, "Chase ****6742 still exists in bankAccounts."

    # Check that backupPaymentMethod is cleared
    wallet_prefs = state.get("walletPreferences", {})
    backup_method = wallet_prefs.get("backupPaymentMethod")
    if backup_method is not None:
        return False, f"walletPreferences.backupPaymentMethod is '{backup_method}', expected None/null after removing the backup bank account."

    return True, "Chase ****6742 removed and backupPaymentMethod cleared."
