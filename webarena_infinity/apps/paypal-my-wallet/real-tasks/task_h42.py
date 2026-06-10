import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()

    errors = []

    # The only confirmed debit card is Mastercard 7156 (card_002).
    # Visa 8834 (card_005) is debit but pending_confirmation.
    cards = state.get("cards", [])
    mc_7156 = None
    old_preferred = None
    for c in cards:
        if c.get("lastFour") == "7156":
            mc_7156 = c
        if c.get("lastFour") == "4829":
            old_preferred = c

    if mc_7156 is None:
        errors.append("Mastercard 7156 not found in cards.")
    else:
        if mc_7156.get("isPreferred") is not True:
            errors.append(
                f"Mastercard 7156 isPreferred is {mc_7156.get('isPreferred')}, expected True."
            )

    if old_preferred is not None and old_preferred.get("isPreferred") is True:
        errors.append("Visa 4829 should no longer be preferred.")

    # Check walletPreferences
    prefs = state.get("walletPreferences", {})
    if prefs.get("preferredPaymentMethod") != "card_002":
        errors.append(
            f"walletPreferences.preferredPaymentMethod is '{prefs.get('preferredPaymentMethod')}', "
            f"expected 'card_002'."
        )

    if errors:
        return False, " ".join(errors)
    return True, "Preferred payment method set to the only confirmed debit card (Mastercard 7156)."
