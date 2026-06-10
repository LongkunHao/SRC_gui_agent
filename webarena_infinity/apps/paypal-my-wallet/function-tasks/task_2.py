import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()

    cards = state.get("cards", [])

    # Find Amex ****3001
    new_backup = None
    for card in cards:
        if card.get("lastFour") == "3001":
            new_backup = card
            break

    if new_backup is None:
        return False, "Card with lastFour '3001' not found in cards."

    if not new_backup.get("isBackup"):
        return False, f"Card ****3001 isBackup is {new_backup.get('isBackup')}, expected True."

    # Check walletPreferences.backupPaymentMethod
    wallet_prefs = state.get("walletPreferences", {})
    backup_method = wallet_prefs.get("backupPaymentMethod")
    if backup_method != new_backup.get("id"):
        return False, f"walletPreferences.backupPaymentMethod is '{backup_method}', expected '{new_backup.get('id')}'."

    # Check currentUser.backupPaymentMethodId
    current_user = state.get("currentUser", {})
    user_backup = current_user.get("backupPaymentMethodId")
    if user_backup != new_backup.get("id"):
        return False, f"currentUser.backupPaymentMethodId is '{user_backup}', expected '{new_backup.get('id')}'."

    # Old backup card ****2290 should no longer be backup
    old_backup = None
    for card in cards:
        if card.get("lastFour") == "2290":
            old_backup = card
            break

    if old_backup is not None and old_backup.get("isBackup"):
        return False, "Old backup card ****2290 still has isBackup=True."

    return True, "Amex ****3001 is now the backup payment method."
