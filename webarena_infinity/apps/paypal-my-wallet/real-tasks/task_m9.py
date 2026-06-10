import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()

    errors = []

    cards = state.get("cards")
    if not cards:
        return False, "No cards found in state."

    # Find the American Express card ending in 3001
    amex_3001 = None
    for card in cards:
        if card.get("lastFour") == "3001":
            amex_3001 = card
            break

    if amex_3001 is None:
        return False, "American Express card ending in 3001 not found in cards."

    if amex_3001.get("isBackup") is not True:
        errors.append(
            f"American Express 3001 is not set as backup (isBackup={amex_3001.get('isBackup')})."
        )

    # Check walletPreferences.backupPaymentMethod matches card_003 id
    prefs = state.get("walletPreferences")
    if prefs is None:
        errors.append("No walletPreferences found in state.")
    else:
        if prefs.get("backupPaymentMethod") != amex_3001.get("id"):
            errors.append(
                f"walletPreferences.backupPaymentMethod is '{prefs.get('backupPaymentMethod')}', "
                f"expected '{amex_3001.get('id')}'."
            )

    # Check old backup card (Mastercard 2290) no longer has isBackup=True
    mc_2290 = None
    for card in cards:
        if card.get("lastFour") == "2290":
            mc_2290 = card
            break

    if mc_2290 is not None and mc_2290.get("isBackup") is True:
        errors.append("Old backup card (Mastercard 2290) still has isBackup=True.")

    if errors:
        return False, " ".join(errors)
    return True, "American Express card ending in 3001 successfully set as backup payment method."
