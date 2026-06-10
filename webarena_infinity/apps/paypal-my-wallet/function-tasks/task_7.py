import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()

    cards = state.get("cards", [])

    for card in cards:
        if card.get("lastFour") == "4829":
            return False, "Preferred Visa card ****4829 still exists in cards."

    # Check that preferredPaymentMethod is cleared
    wallet_prefs = state.get("walletPreferences", {})
    pref_method = wallet_prefs.get("preferredPaymentMethod")
    if pref_method is not None:
        return False, f"walletPreferences.preferredPaymentMethod is '{pref_method}', expected None/null after removing the preferred card."

    return True, "Visa ****4829 removed and preferredPaymentMethod cleared."
