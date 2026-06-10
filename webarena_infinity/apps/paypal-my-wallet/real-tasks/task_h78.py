import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()

    errors = []

    # Active Pay in 4 plans: Nordstrom (active) and Nike (active) = 2
    # 2 * $25 = $50 Starbucks gift card for self

    gift_cards = state.get("giftCards", [])
    seed_gc_ids = {"gc_001", "gc_002", "gc_003", "gc_004", "gc_005"}
    new_sbx_gcs = [
        gc for gc in gift_cards
        if gc.get("id") not in seed_gc_ids
        and gc.get("merchantName") == "Starbucks"
        and gc.get("amount") == 50
    ]
    if not new_sbx_gcs:
        errors.append(
            "No new $50 Starbucks gift card found "
            "(expected 2 active plans × $25 = $50)."
        )
    else:
        gc = new_sbx_gcs[0]
        user_email = state.get("currentUser", {}).get("email", "")
        if gc.get("recipientEmail") != user_email:
            errors.append(
                f"Starbucks gift card recipient is '{gc.get('recipientEmail')}', "
                f"expected '{user_email}' (self)."
            )

    # Should have a gift_card transaction for Starbucks $50
    transactions = state.get("transactions", [])
    found_gc_txn = any(
        t.get("type") == "gift_card"
        and "Starbucks" in (t.get("description") or "")
        and t.get("amount") == -50
        for t in transactions
    )
    if not found_gc_txn:
        errors.append("No gift_card transaction for $50 Starbucks found.")

    if errors:
        return False, " ".join(errors)
    return True, "Bought $50 Starbucks gift card (2 active plans × $25) for self."
