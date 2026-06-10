import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()

    errors = []

    offers = state.get("offers", [])
    if not offers:
        return False, "No offers found in state."

    # Previously saved offers should now be 'available' (unsaved):
    # Starbucks (offer_001), Uber (offer_002), Spotify (offer_007)
    for merchant in ["Starbucks", "Uber", "Spotify"]:
        offer = None
        for o in offers:
            if o.get("merchantName") == merchant:
                offer = o
                break
        if offer is None:
            errors.append(f"{merchant} offer not found.")
        elif offer.get("status") != "available":
            errors.append(
                f"{merchant} offer status is '{offer.get('status')}', expected 'available' "
                f"(should have been unsaved)."
            )

    # Target, Nike, Amazon should now be 'saved'
    for merchant in ["Target", "Nike", "Amazon"]:
        offer = None
        for o in offers:
            if o.get("merchantName") == merchant:
                offer = o
                break
        if offer is None:
            errors.append(f"{merchant} offer not found.")
        elif offer.get("status") != "saved":
            errors.append(
                f"{merchant} offer status is '{offer.get('status')}', expected 'saved'."
            )

    if errors:
        return False, " ".join(errors)
    return True, "Unsaved previous offers and saved Target, Nike, and Amazon instead."
