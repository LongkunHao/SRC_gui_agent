import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()

    offers = state.get("offers")
    if offers is None:
        return False, "offers not found in state."

    amazon_offer = None
    for offer in offers:
        name = offer.get("merchantName", "")
        if "Amazon" == name:
            amazon_offer = offer
            break

    if amazon_offer is None:
        return False, "Amazon offer not found in offers list."

    if amazon_offer.get("status") != "saved":
        return False, f"Amazon offer status is '{amazon_offer.get('status')}', expected 'saved'."

    return True, "Amazon cashback deal has been bookmarked (saved)."
