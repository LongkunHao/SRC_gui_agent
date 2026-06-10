import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()

    offers = state.get("offers", [])
    if not isinstance(offers, list):
        return False, f"Expected offers to be a list, got {type(offers).__name__}."

    walmart_offer = None
    for offer in offers:
        if offer.get("merchantName", "").lower() == "walmart":
            walmart_offer = offer
            break

    if walmart_offer is None:
        return False, "Could not find an offer with merchantName 'Walmart'."

    status = walmart_offer.get("status", "")
    if status != "saved":
        return False, f"Expected Walmart offer status to be 'saved', got '{status}'."

    saved_at = walmart_offer.get("savedAt")
    if saved_at is None:
        return False, "Expected Walmart offer savedAt to be set, but it is None."

    return True, "Walmart offer has been successfully saved."
