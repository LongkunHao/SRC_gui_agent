import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()

    errors = []

    # Check cashback category changed to Groceries
    debit = state.get("paypalDebitCard")
    if debit is None:
        errors.append("PayPal Debit Card not found.")
    else:
        if debit.get("cashBackCategory") != "Groceries":
            errors.append(
                f"Cashback category is '{debit.get('cashBackCategory')}', "
                f"expected 'Groceries'."
            )

    # Check for new Uber gift card for self ($25)
    gift_cards = state.get("giftCards", [])
    seed_gc_ids = {"gc_001", "gc_002", "gc_003", "gc_004", "gc_005"}
    found_gc = False
    for gc in gift_cards:
        if gc.get("id") not in seed_gc_ids:
            if gc.get("merchantName") == "Uber" and gc.get("amount") == 25:
                user = state.get("currentUser", {})
                if gc.get("recipientEmail") == user.get("email"):
                    found_gc = True
                    break
    if not found_gc:
        errors.append("No new $25 Uber gift card for self found.")

    if errors:
        return False, " ".join(errors)
    return True, "Changed cashback category to Groceries and bought $25 Uber gift card for self."
