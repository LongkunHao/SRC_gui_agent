import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()

    errors = []

    # Find the new Nike gift card
    gift_cards = state.get("giftCards", [])
    # Seed gift card IDs: gc_001 through gc_005
    seed_gc_ids = {"gc_001", "gc_002", "gc_003", "gc_004", "gc_005"}
    nike_gc = None
    for gc in gift_cards:
        if gc.get("id") not in seed_gc_ids:
            merchant = gc.get("merchantName", "")
            if merchant.lower() == "nike":
                nike_gc = gc
                break

    if nike_gc is None:
        # Also check by merchant name in case IDs were reused
        for gc in gift_cards:
            if gc.get("merchantName", "").lower() == "nike" and gc.get("id") not in seed_gc_ids:
                nike_gc = gc
                break

    if nike_gc is None:
        errors.append("No new Nike gift card found in giftCards.")
    else:
        if nike_gc.get("amount") != 50:
            errors.append(f"Nike gift card amount is {nike_gc.get('amount')}, expected 50.")

        actual_email = nike_gc.get("recipientEmail", "")
        if actual_email.lower() != "riley.p@email.com":
            errors.append(
                f"Nike gift card recipientEmail is '{actual_email}', expected 'riley.p@email.com'."
            )

        actual_name = nike_gc.get("recipientName", "")
        if actual_name.lower() != "riley parker":
            errors.append(
                f"Nike gift card recipientName is '{actual_name}', expected 'Riley Parker'."
            )

        actual_msg = nike_gc.get("message", "")
        if "happy holidays" not in actual_msg.lower():
            errors.append(
                f"Nike gift card message is '{actual_msg}', expected 'Happy Holidays!'."
            )

        if nike_gc.get("status") != "active":
            errors.append(f"Nike gift card status is '{nike_gc.get('status')}', expected 'active'.")

    # Check USD balance decreased by 50
    balances = state.get("balances", [])
    usd_bal = None
    for b in balances:
        if b.get("currency") == "USD":
            usd_bal = b
            break

    if usd_bal is None:
        errors.append("USD balance not found.")
    else:
        actual_usd = usd_bal.get("amount", 0)
        expected_usd = round(2847.63 - 50, 2)
        if actual_usd > expected_usd + 1.0:
            errors.append(
                f"USD balance is {actual_usd}, expected approximately {expected_usd} or less "
                f"(seed 2847.63 minus 50)."
            )

    # Check for gift_card transaction
    transactions = state.get("transactions", [])
    gc_txn = None
    for t in transactions:
        if t.get("type") == "gift_card":
            desc = t.get("description", "").lower()
            if "nike" in desc:
                gc_txn = t
                break

    if gc_txn is None:
        errors.append("No gift_card transaction found for Nike.")

    if errors:
        return False, " ".join(errors)
    return True, "Successfully sent $50 Nike gift card to Riley Parker at riley.p@email.com with message 'Happy Holidays!'."
