import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()

    errors = []

    cards = state.get("cards", [])
    if not cards:
        return False, "No cards found in state."

    # Find Amex 3001 (card_003) - should now be preferred
    amex_3001 = None
    for c in cards:
        if c.get("lastFour") == "3001":
            amex_3001 = c
            break

    if amex_3001 is None:
        errors.append("American Express card ending in 3001 not found.")
    else:
        if amex_3001.get("isPreferred") is not True:
            errors.append(
                f"Amex 3001 isPreferred is {amex_3001.get('isPreferred')}, expected True."
            )

    # Find old preferred Visa 4829 (card_001) - should no longer be preferred
    visa_4829 = None
    for c in cards:
        if c.get("lastFour") == "4829":
            visa_4829 = c
            break

    if visa_4829 is not None and visa_4829.get("isPreferred") is True:
        errors.append("Old preferred card (Visa 4829) still has isPreferred=True.")

    # Check walletPreferences.preferredPaymentMethod is card_003
    prefs = state.get("walletPreferences")
    if prefs is None:
        errors.append("No walletPreferences found in state.")
    else:
        pref_method = prefs.get("preferredPaymentMethod")
        if pref_method != "card_003":
            errors.append(
                f"walletPreferences.preferredPaymentMethod is '{pref_method}', expected 'card_003'."
            )

        # Check backup is bank_004 (Citibank 1104)
        backup_method = prefs.get("backupPaymentMethod")
        if backup_method != "bank_004":
            errors.append(
                f"walletPreferences.backupPaymentMethod is '{backup_method}', expected 'bank_004'."
            )

    # Check old backup card MC 2290 (card_006) is no longer backup
    mc_2290 = None
    for c in cards:
        if c.get("lastFour") == "2290":
            mc_2290 = c
            break

    if mc_2290 is not None and mc_2290.get("isBackup") is True:
        errors.append("Old backup card (Mastercard 2290) still has isBackup=True.")

    if errors:
        return False, " ".join(errors)
    return True, "Preferred payment switched to Amex 3001 and backup set to Citibank checking (bank_004)."
