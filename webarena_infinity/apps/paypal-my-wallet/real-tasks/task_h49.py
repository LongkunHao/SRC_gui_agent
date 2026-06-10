import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()

    errors = []

    # Check for new Nike gift card to jamie@email.com with "Great job!"
    gift_cards = state.get("giftCards", [])
    seed_gc_ids = {"gc_001", "gc_002", "gc_003", "gc_004", "gc_005"}
    found_gc = False
    for gc in gift_cards:
        if gc.get("id") not in seed_gc_ids:
            if (gc.get("merchantName") == "Nike"
                    and gc.get("amount") == 50
                    and gc.get("recipientEmail") == "jamie@email.com"
                    and gc.get("message") == "Great job!"):
                found_gc = True
                break
    if not found_gc:
        errors.append(
            "No new Nike $50 gift card for jamie@email.com with message 'Great job!' found."
        )

    # Check DoorDash offer is saved
    offers = state.get("offers", [])
    doordash = None
    for o in offers:
        if o.get("merchantName") == "DoorDash":
            doordash = o
            break

    if doordash is None:
        errors.append("DoorDash offer not found.")
    elif doordash.get("status") != "saved":
        errors.append(
            f"DoorDash offer status is '{doordash.get('status')}', expected 'saved'."
        )

    if errors:
        return False, " ".join(errors)
    return True, "Sent $50 Nike gift card to jamie@email.com and saved DoorDash offer."
