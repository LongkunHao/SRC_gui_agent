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

    # Available offers with percentage-based cashback >= 10%:
    #   DoorDash: 15% (available) -> should be saved
    #   Lyft: 12% (available) -> should be saved
    # Offers that should NOT be saved (< 10% or non-percentage or not available):
    #   Nike: 8% -> should remain available
    #   Target: 5% -> should remain available
    #   Starbucks: 10% but already saved -> should stay saved (not newly changed)
    should_be_saved = ["DoorDash", "Lyft"]
    should_not_be_saved = ["Nike", "Target", "Walmart", "Amazon"]

    for merchant in should_be_saved:
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

    for merchant in should_not_be_saved:
        offer = None
        for o in offers:
            if o.get("merchantName") == merchant:
                offer = o
                break
        if offer is not None and offer.get("status") == "saved":
            errors.append(
                f"{merchant} offer was saved but its cashback is below 10% "
                f"(should remain available)."
            )

    if errors:
        return False, " ".join(errors)
    return True, "Saved all available offers with percentage-based cashback >= 10%."
