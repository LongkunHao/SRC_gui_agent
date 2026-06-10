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

    # Find the Mastercard ending in 7156
    mc_7156 = None
    for card in cards:
        if card.get("lastFour") == "7156":
            mc_7156 = card
            break

    if mc_7156 is None:
        return False, "Mastercard ending in 7156 not found in cards."

    if mc_7156.get("isPreferred") is not True:
        errors.append(f"Mastercard 7156 is not set as preferred (isPreferred={mc_7156.get('isPreferred')}).")

    # Check that the old preferred card (Visa 4829) is no longer preferred
    visa_4829 = None
    for card in cards:
        if card.get("lastFour") == "4829":
            visa_4829 = card
            break

    if visa_4829 is not None and visa_4829.get("isPreferred") is True:
        errors.append("Old preferred card (Visa 4829) still has isPreferred=True.")

    # Check walletPreferences.preferredPaymentMethod matches the card's id
    prefs = state.get("walletPreferences")
    if prefs is None:
        errors.append("No walletPreferences found in state.")
    else:
        if prefs.get("preferredPaymentMethod") != mc_7156.get("id"):
            errors.append(
                f"walletPreferences.preferredPaymentMethod is '{prefs.get('preferredPaymentMethod')}', "
                f"expected '{mc_7156.get('id')}'."
            )

    # Check currentUser.preferredPaymentMethodId matches
    current_user = state.get("currentUser")
    if current_user is None:
        errors.append("No currentUser found in state.")
    else:
        if current_user.get("preferredPaymentMethodId") != mc_7156.get("id"):
            errors.append(
                f"currentUser.preferredPaymentMethodId is '{current_user.get('preferredPaymentMethodId')}', "
                f"expected '{mc_7156.get('id')}'."
            )

    if errors:
        return False, " ".join(errors)
    return True, "Preferred payment method successfully switched to Mastercard ending in 7156."
