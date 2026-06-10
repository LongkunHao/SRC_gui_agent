import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()

    offers = state.get("offers")
    if offers is None:
        return False, "offers not found in state."

    nike_offer = None
    for offer in offers:
        name = offer.get("merchantName", "")
        if "Nike" == name:
            nike_offer = offer
            break

    if nike_offer is None:
        return False, "Nike offer not found in offers list."

    if nike_offer.get("status") != "saved":
        return False, f"Nike offer status is '{nike_offer.get('status')}', expected 'saved'."

    return True, "Nike cashback offer has been saved."
