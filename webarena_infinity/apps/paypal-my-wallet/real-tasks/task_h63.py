import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()

    errors = []

    offers = state.get("offers", [])

    # Available offers with maxCashback >= 15 (from seed):
    # DoorDash: maxCashback 15, available
    # Nike: maxCashback 50, available
    # Target: maxCashback 25, available
    # Walmart: maxCashback 20, available
    # Lyft: maxCashback 15, available
    # Amazon: maxCashback 40, available
    should_be_saved = {"DoorDash", "Nike", "Target", "Walmart", "Lyft", "Amazon"}

    for offer in offers:
        name = offer.get("merchantName", "")
        if name in should_be_saved:
            if offer.get("status") != "saved":
                errors.append(
                    f"Offer '{name}' (maxCashback >= $15) should be saved, "
                    f"but status is '{offer.get('status')}'."
                )

    # Offers that should NOT have been saved (maxCashback < 15 and were available):
    # Chipotle: maxCashback $2
    should_not_be_saved = {"Chipotle"}
    for offer in offers:
        name = offer.get("merchantName", "")
        if name in should_not_be_saved:
            if offer.get("status") == "saved" and offer.get("savedAt") is not None:
                # Check if it was already saved before (Chipotle was available in seed)
                errors.append(
                    f"Offer '{name}' (maxCashback < $15) should NOT have been saved."
                )

    if errors:
        return False, " ".join(errors)
    return True, "Saved all available offers with maximum cashback >= $15."
