import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()

    # Find the card with lastFour == '3001' (Amex)
    cards = state.get("cards", [])
    amex_card = None
    old_preferred_card = None
    for card in cards:
        if card.get("lastFour") == "3001":
            amex_card = card
        if card.get("lastFour") == "4829":
            old_preferred_card = card

    if amex_card is None:
        return False, "Could not find a card with lastFour '3001' (Amex)."

    amex_id = amex_card.get("id", "")

    # Check walletPreferences.preferredPaymentMethod
    prefs = state.get("walletPreferences", {})
    preferred = prefs.get("preferredPaymentMethod", "")
    if preferred != amex_id:
        return False, f"Expected walletPreferences.preferredPaymentMethod to be '{amex_id}', got '{preferred}'."

    # Check currentUser.preferredPaymentMethodId
    current_user = state.get("currentUser", {})
    user_preferred = current_user.get("preferredPaymentMethodId", "")
    if user_preferred != amex_id:
        return False, f"Expected currentUser.preferredPaymentMethodId to be '{amex_id}', got '{user_preferred}'."

    # Check that Amex card has isPreferred == True
    if not amex_card.get("isPreferred"):
        return False, f"Expected card with lastFour '3001' to have isPreferred=True, got {amex_card.get('isPreferred')}."

    # Check that old preferred card (lastFour 4829) has isPreferred == False
    if old_preferred_card is not None:
        if old_preferred_card.get("isPreferred"):
            return False, f"Expected card with lastFour '4829' to have isPreferred=False, got {old_preferred_card.get('isPreferred')}."

    return True, "Preferred payment method successfully set to Amex ****3001."
