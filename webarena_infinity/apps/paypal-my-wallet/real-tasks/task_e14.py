import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()

    offers = state.get("offers")
    if offers is None:
        return False, "offers not found in state."

    spotify_offer = None
    for offer in offers:
        name = offer.get("merchantName", "")
        if "Spotify" == name:
            spotify_offer = offer
            break

    if spotify_offer is None:
        return False, "Spotify offer not found in offers list."

    if spotify_offer.get("status") != "available":
        return False, f"Spotify offer status is '{spotify_offer.get('status')}', expected 'available'."

    if spotify_offer.get("savedAt") is not None:
        return False, f"Spotify offer savedAt is '{spotify_offer.get('savedAt')}', expected None."

    return True, "Spotify offer has been removed from saved list."
