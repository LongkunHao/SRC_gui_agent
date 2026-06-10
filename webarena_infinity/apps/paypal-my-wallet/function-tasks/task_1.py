import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()

    cards = state.get("cards", [])

    # Find the Mastercard ****7156
    new_preferred = None
    for card in cards:
        if card.get("lastFour") == "7156":
            new_preferred = card
            break

    if new_preferred is None:
        return False, "Card with lastFour '7156' not found in cards."

    if not new_preferred.get("isPreferred"):
        return False, f"Card ****7156 isPreferred is {new_preferred.get('isPreferred')}, expected True."

    # Check walletPreferences.preferredPaymentMethod
    wallet_prefs = state.get("walletPreferences", {})
    pref_method = wallet_prefs.get("preferredPaymentMethod")
    if pref_method != new_preferred.get("id"):
        return False, f"walletPreferences.preferredPaymentMethod is '{pref_method}', expected '{new_preferred.get('id')}'."

    # Check currentUser.preferredPaymentMethodId
    current_user = state.get("currentUser", {})
    user_pref = current_user.get("preferredPaymentMethodId")
    if user_pref != new_preferred.get("id"):
        return False, f"currentUser.preferredPaymentMethodId is '{user_pref}', expected '{new_preferred.get('id')}'."

    # Old preferred card ****4829 should no longer be preferred
    old_preferred = None
    for card in cards:
        if card.get("lastFour") == "4829":
            old_preferred = card
            break

    if old_preferred is not None and old_preferred.get("isPreferred"):
        return False, "Old preferred card ****4829 still has isPreferred=True."

    return True, "Mastercard ****7156 is now the preferred payment method."
