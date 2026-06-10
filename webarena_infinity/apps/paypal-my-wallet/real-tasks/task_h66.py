import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()

    errors = []

    cards = state.get("cards", [])

    # Confirmed non-expired cards and their expirations:
    # Visa 4829: 09/2028
    # MC 7156: 03/2027
    # AmEx 3001: 12/2026 (soonest)
    # MC 2290: 08/2028
    # The soonest-expiring confirmed card is AmEx 3001 (12/2026).

    amex_3001 = None
    for c in cards:
        if c.get("lastFour") == "3001":
            amex_3001 = c
            break

    if amex_3001 is None:
        errors.append("American Express 3001 not found in cards.")
    else:
        if not amex_3001.get("isBackup"):
            errors.append(
                "American Express 3001 (soonest expiring confirmed card) "
                "should be set as backup payment method."
            )

    # walletPreferences should reflect AmEx 3001 as backup
    prefs = state.get("walletPreferences", {})
    if amex_3001 and prefs.get("backupPaymentMethod") != amex_3001.get("id"):
        errors.append(
            f"Wallet backup payment is '{prefs.get('backupPaymentMethod')}', "
            f"expected '{amex_3001.get('id') if amex_3001 else 'card_003'}'."
        )

    # currentUser should also reflect the backup
    user = state.get("currentUser", {})
    if amex_3001 and user.get("backupPaymentMethodId") != amex_3001.get("id"):
        errors.append(
            f"User backup payment ID is '{user.get('backupPaymentMethodId')}', "
            f"expected '{amex_3001.get('id') if amex_3001 else 'card_003'}'."
        )

    if errors:
        return False, " ".join(errors)
    return True, "Set American Express 3001 (soonest expiring confirmed card) as backup payment method."
