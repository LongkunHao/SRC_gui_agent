import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()

    offers = state.get("offers")
    if offers is None:
        return False, "offers not found in state."

    starbucks_offer = None
    for offer in offers:
        name = offer.get("merchantName", "")
        if "Starbucks" == name:
            starbucks_offer = offer
            break

    if starbucks_offer is None:
        return False, "Starbucks offer not found in offers list."

    if starbucks_offer.get("status") != "available":
        return False, f"Starbucks offer status is '{starbucks_offer.get('status')}', expected 'available'."

    if starbucks_offer.get("savedAt") is not None:
        return False, f"Starbucks offer savedAt is '{starbucks_offer.get('savedAt')}', expected None."

    return True, "Starbucks offer has been removed from saved list."
