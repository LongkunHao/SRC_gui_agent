import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()

    errors = []

    # Step 1: All available Food & Drink offers should be saved.
    # From seed, available Food & Drink: DoorDash (offer_003), Chipotle (offer_012)
    offers = state.get("offers", [])
    food_drink_available = {"DoorDash", "Chipotle"}
    for offer in offers:
        name = offer.get("merchantName", "")
        if name in food_drink_available:
            if offer.get("status") != "saved":
                errors.append(
                    f"Food & Drink offer '{name}' should be saved, "
                    f"but status is '{offer.get('status')}'."
                )

    # Step 2: Should have a new $25 DoorDash gift card for self
    gift_cards = state.get("giftCards", [])
    seed_gc_ids = {"gc_001", "gc_002", "gc_003", "gc_004", "gc_005"}
    new_dd_gcs = [
        gc for gc in gift_cards
        if gc.get("id") not in seed_gc_ids
        and gc.get("merchantName") == "DoorDash"
        and gc.get("amount") == 25
    ]
    if not new_dd_gcs:
        errors.append("No new $25 DoorDash gift card found.")
    else:
        gc = new_dd_gcs[0]
        user_email = state.get("currentUser", {}).get("email", "")
        if gc.get("recipientEmail") != user_email:
            errors.append(
                f"DoorDash gift card recipient is '{gc.get('recipientEmail')}', "
                f"expected '{user_email}' (self)."
            )

    # Step 3: Currency conversion should be set to card_issuer
    prefs = state.get("walletPreferences", {})
    if prefs.get("currencyConversionOption") != "card_issuer":
        errors.append(
            f"Currency conversion is '{prefs.get('currencyConversionOption')}', "
            f"expected 'card_issuer'."
        )

    if errors:
        return False, " ".join(errors)
    return True, "Saved Food & Drink offers, bought $25 DoorDash gift card, switched to card issuer conversion."
