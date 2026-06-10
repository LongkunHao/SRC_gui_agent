import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()

    errors = []

    # Find the new Best Buy gift card
    gift_cards = state.get("giftCards", [])
    seed_gc_ids = {"gc_001", "gc_002", "gc_003", "gc_004", "gc_005"}
    best_buy_gc = None
    for gc in gift_cards:
        merchant = gc.get("merchantName", "").lower()
        if merchant == "best buy" and gc.get("id") not in seed_gc_ids:
            best_buy_gc = gc
            break

    if best_buy_gc is None:
        errors.append("No new Best Buy gift card found in giftCards.")
    else:
        if best_buy_gc.get("amount") != 100:
            errors.append(f"Best Buy gift card amount is {best_buy_gc.get('amount')}, expected 100.")

        actual_email = best_buy_gc.get("recipientEmail", "")
        if actual_email.lower() != "mark.taylor@email.com":
            errors.append(
                f"Best Buy gift card recipientEmail is '{actual_email}', expected 'mark.taylor@email.com'."
            )

        actual_msg = best_buy_gc.get("message", "")
        if "congrats on the promotion" not in actual_msg.lower():
            errors.append(
                f"Best Buy gift card message is '{actual_msg}', expected 'Congrats on the promotion!'."
            )

        if best_buy_gc.get("status") != "active":
            errors.append(
                f"Best Buy gift card status is '{best_buy_gc.get('status')}', expected 'active'."
            )

    # Check USD balance decreased by 100
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
        expected_usd = round(2847.63 - 100, 2)
        if actual_usd > expected_usd + 1.0:
            errors.append(
                f"USD balance is {actual_usd}, expected approximately {expected_usd} or less "
                f"(seed 2847.63 minus 100)."
            )

    # Check for gift_card transaction for Best Buy
    transactions = state.get("transactions", [])
    gc_txn = None
    for t in transactions:
        if t.get("type") == "gift_card":
            desc = t.get("description", "").lower()
            if "best buy" in desc:
                gc_txn = t
                break

    if gc_txn is None:
        errors.append("No gift_card transaction found for Best Buy.")

    if errors:
        return False, " ".join(errors)
    return True, "Successfully purchased $100 Best Buy gift card for mark.taylor@email.com with message 'Congrats on the promotion!'."
