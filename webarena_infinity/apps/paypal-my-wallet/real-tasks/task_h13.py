import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()

    errors = []

    # Check walletPreferences.currencyConversionOption == "card_issuer"
    prefs = state.get("walletPreferences")
    if prefs is None:
        errors.append("No walletPreferences found in state.")
    else:
        conversion_option = prefs.get("currencyConversionOption")
        if conversion_option != "card_issuer":
            errors.append(
                f"walletPreferences.currencyConversionOption is '{conversion_option}', "
                f"expected 'card_issuer'."
            )

    # Find MC 2290 card
    cards = state.get("cards", [])
    mc_2290 = None
    visa_4829 = None
    for card in cards:
        if card.get("lastFour") == "2290":
            mc_2290 = card
        if card.get("lastFour") == "4829":
            visa_4829 = card

    if mc_2290 is None:
        errors.append("Mastercard ending in 2290 not found in cards.")
    else:
        # Check MC 2290 is preferred
        if mc_2290.get("isPreferred") is not True:
            errors.append(
                f"Mastercard 2290 isPreferred is {mc_2290.get('isPreferred')}, expected True."
            )

        # Check walletPreferences.preferredPaymentMethod matches MC 2290 id
        if prefs is not None:
            preferred_method = prefs.get("preferredPaymentMethod")
            if preferred_method != mc_2290.get("id"):
                errors.append(
                    f"walletPreferences.preferredPaymentMethod is '{preferred_method}', "
                    f"expected '{mc_2290.get('id')}'."
                )

    # Check old preferred card (Visa 4829) is no longer preferred
    if visa_4829 is None:
        errors.append("Visa ending in 4829 not found in cards.")
    else:
        if visa_4829.get("isPreferred") is True:
            errors.append(
                "Old preferred card (Visa 4829) still has isPreferred=True."
            )

    if errors:
        return False, " ".join(errors)
    return True, "Successfully switched currency conversion to card issuer and made MC 2290 the preferred payment method."
