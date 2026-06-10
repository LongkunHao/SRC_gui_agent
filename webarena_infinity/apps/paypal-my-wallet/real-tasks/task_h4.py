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

    # Find DoorDash offer (offer_003) and Chipotle offer (offer_012)
    # Both are Food & Drink category and had status "available" in seed data
    doordash = None
    chipotle = None
    for o in offers:
        name = o.get("merchantName", "").lower()
        if name == "doordash":
            doordash = o
        elif name == "chipotle":
            chipotle = o

    if doordash is None:
        errors.append("DoorDash offer not found in offers.")
    else:
        if doordash.get("status") != "saved":
            errors.append(
                f"DoorDash offer status is '{doordash.get('status')}', expected 'saved'."
            )

    if chipotle is None:
        errors.append("Chipotle offer not found in offers.")
    else:
        if chipotle.get("status") != "saved":
            errors.append(
                f"Chipotle offer status is '{chipotle.get('status')}', expected 'saved'."
            )

    if errors:
        return False, " ".join(errors)
    return True, "Both Food & Drink offers (DoorDash and Chipotle) have been saved successfully."
