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

    # Check Target offer status == "saved"
    target_offer = None
    walmart_offer = None
    lyft_offer = None
    for offer in offers:
        name = (offer.get("merchantName") or "").lower()
        if name == "target":
            target_offer = offer
        elif name == "walmart":
            walmart_offer = offer
        elif name == "lyft":
            lyft_offer = offer

    if target_offer is None:
        errors.append("Target offer not found in offers.")
    elif target_offer.get("status") != "saved":
        errors.append(
            f"Target offer status is '{target_offer.get('status')}', expected 'saved'."
        )

    if walmart_offer is None:
        errors.append("Walmart offer not found in offers.")
    elif walmart_offer.get("status") != "saved":
        errors.append(
            f"Walmart offer status is '{walmart_offer.get('status')}', expected 'saved'."
        )

    if lyft_offer is None:
        errors.append("Lyft offer not found in offers.")
    elif lyft_offer.get("status") != "saved":
        errors.append(
            f"Lyft offer status is '{lyft_offer.get('status')}', expected 'saved'."
        )

    if errors:
        return False, " ".join(errors)
    return True, "Successfully saved Target, Walmart, and Lyft offers."
