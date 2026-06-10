import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()

    errors = []

    # Check Chipotle offer is saved
    offers = state.get("offers", [])
    chipotle = None
    for o in offers:
        if o.get("merchantName") == "Chipotle":
            chipotle = o
            break

    if chipotle is None:
        errors.append("Chipotle offer not found.")
    elif chipotle.get("status") != "saved":
        errors.append(
            f"Chipotle offer status is '{chipotle.get('status')}', expected 'saved'."
        )

    # Check for new DoorDash $25 gift card (self-purchase)
    gift_cards = state.get("giftCards", [])
    user_email = "jordan.mitchell@outlook.com"
    doordash_gc = None
    for gc in gift_cards:
        if (gc.get("merchantName", "").lower() == "doordash"
                and gc.get("amount") == 25
                and gc.get("status") == "active"):
            doordash_gc = gc
            break

    if doordash_gc is None:
        errors.append("No active DoorDash $25 gift card found.")
    else:
        if doordash_gc.get("recipientEmail") != user_email:
            errors.append(
                f"DoorDash gift card recipient is '{doordash_gc.get('recipientEmail')}', "
                f"expected '{user_email}' (self-purchase)."
            )

    if errors:
        return False, " ".join(errors)
    return True, "Chipotle offer saved and $25 DoorDash gift card purchased for self."
