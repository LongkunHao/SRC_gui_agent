import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()

    errors = []

    cards = state.get("cards", [])
    remaining_last_fours = {c.get("lastFour") for c in cards}

    # Most recently added confirmed credit card is MC 2290 (card_006, added 2022-09-15).
    # It should now be preferred.
    mc_2290 = None
    for c in cards:
        if c.get("lastFour") == "2290":
            mc_2290 = c
            break

    if mc_2290 is None:
        errors.append("Mastercard 2290 not found in cards.")
    else:
        if not mc_2290.get("isPreferred"):
            errors.append("Mastercard 2290 should be set as preferred payment method.")

    # walletPreferences should reflect MC 2290 as preferred
    prefs = state.get("walletPreferences", {})
    if mc_2290 and prefs.get("preferredPaymentMethod") != mc_2290.get("id"):
        errors.append(
            f"Wallet preferred payment is '{prefs.get('preferredPaymentMethod')}', "
            f"expected '{mc_2290.get('id') if mc_2290 else 'card_006'}'."
        )

    # Oldest credit card is Visa 4829 (card_001, added 2019-03-14). Should be removed.
    if "4829" in remaining_last_fours:
        errors.append("Visa 4829 (oldest credit card) should have been removed.")

    # Other cards should remain
    for lf in ["7156", "8834", "3001", "2290"]:
        if lf not in remaining_last_fours:
            errors.append(f"Card ending in {lf} was removed but should have been kept.")

    if errors:
        return False, " ".join(errors)
    return True, "Set most recently added confirmed credit card (MC 2290) as preferred and removed oldest credit card (Visa 4829)."
