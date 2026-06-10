import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()

    errors = []

    prefs = state.get("walletPreferences", {})

    # Backup should be Bank of America (bank_002)
    banks = state.get("bankAccounts", [])
    boa = None
    for b in banks:
        if b.get("bankName") == "Bank of America":
            boa = b
            break

    if boa is None:
        errors.append("Bank of America account not found.")
    else:
        if prefs.get("backupPaymentMethod") != boa.get("id"):
            errors.append(
                f"Backup payment method is '{prefs.get('backupPaymentMethod')}', "
                f"expected '{boa.get('id')}' (Bank of America)."
            )

    # Preferred should be Mastercard 2290 (card_006)
    cards = state.get("cards", [])
    mc2290 = None
    for c in cards:
        if c.get("lastFour") == "2290":
            mc2290 = c
            break

    if mc2290 is None:
        errors.append("Mastercard ending in 2290 not found.")
    else:
        if not mc2290.get("isPreferred"):
            errors.append("Mastercard 2290 is not set as preferred.")
        if prefs.get("preferredPaymentMethod") != mc2290.get("id"):
            errors.append(
                f"Preferred payment method is '{prefs.get('preferredPaymentMethod')}', "
                f"expected '{mc2290.get('id')}' (Mastercard 2290)."
            )

    if errors:
        return False, " ".join(errors)
    return True, "Bank of America set as backup and Mastercard 2290 set as preferred."
