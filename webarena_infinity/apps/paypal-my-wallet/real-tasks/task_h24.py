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

    # Shopping category offers that were available in seed:
    # Nike (offer_004), Target (offer_006), Walmart (offer_008), Amazon (offer_011)
    shopping_merchants = ["Nike", "Target", "Walmart", "Amazon"]

    for merchant in shopping_merchants:
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
    return True, "All Shopping category offers (Nike, Target, Walmart, Amazon) have been saved."
