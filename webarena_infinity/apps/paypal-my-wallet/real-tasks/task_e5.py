import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()

    offers = state.get("offers")
    if offers is None:
        return False, "No offers found in state."

    uber_offers = [o for o in offers if o.get("merchantName") == "Uber"]
    if not uber_offers:
        return False, "No Uber offer found in state."

    for offer in uber_offers:
        if offer.get("status") != "available":
            return False, f"Uber offer status is '{offer.get('status')}', expected 'available'."
        if offer.get("savedAt") is not None:
            return False, f"Uber offer savedAt is '{offer.get('savedAt')}', expected None."

    return True, "Uber offer has been successfully removed from saved (status is 'available', savedAt is None)."
