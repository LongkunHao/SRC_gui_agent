import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()

    errors = []

    # Check for new Amazon gift card ($50 to sarah.chen@email.com)
    gift_cards = state.get("giftCards", [])
    found_gc = False
    for gc in gift_cards:
        if (gc.get("merchantName", "").lower() == "amazon"
                and gc.get("amount") == 50
                and gc.get("recipientEmail") == "sarah.chen@email.com"
                and gc.get("status") == "active"):
            found_gc = True
            break

    if not found_gc:
        # Check if any Amazon $50 gift card exists
        any_amazon = [gc for gc in gift_cards
                      if gc.get("merchantName", "").lower() == "amazon"
                      and gc.get("amount") == 50
                      and gc.get("id") != "gc_001"]
        if any_amazon:
            gc = any_amazon[0]
            if gc.get("recipientEmail") != "sarah.chen@email.com":
                errors.append(
                    f"Found Amazon $50 gift card but recipient is '{gc.get('recipientEmail')}', "
                    f"expected 'sarah.chen@email.com'."
                )
        else:
            errors.append("No new Amazon $50 gift card found in giftCards.")

    # Check Amazon offer is saved
    offers = state.get("offers", [])
    amazon_offer = None
    for o in offers:
        if o.get("merchantName") == "Amazon":
            amazon_offer = o
            break

    if amazon_offer is None:
        errors.append("Amazon offer not found.")
    elif amazon_offer.get("status") != "saved":
        errors.append(
            f"Amazon offer status is '{amazon_offer.get('status')}', expected 'saved'."
        )

    if errors:
        return False, " ".join(errors)
    return True, "Successfully sent $50 Amazon gift card and saved the Amazon cashback offer."
