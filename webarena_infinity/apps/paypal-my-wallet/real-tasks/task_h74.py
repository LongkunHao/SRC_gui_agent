import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()

    errors = []

    # Most recently purchased active gift card (from seed):
    # gc_004: Netflix $30, purchased 2026-03-05, active (most recent active)
    # gc_001: Amazon $50, purchased 2026-02-14, active
    # gc_005: Home Depot $75, purchased 2026-01-20, active
    # So should buy a $30 Netflix gift card for self.

    gift_cards = state.get("giftCards", [])
    seed_gc_ids = {"gc_001", "gc_002", "gc_003", "gc_004", "gc_005"}
    new_netflix_gcs = [
        gc for gc in gift_cards
        if gc.get("id") not in seed_gc_ids
        and gc.get("merchantName") == "Netflix"
        and gc.get("amount") == 30
    ]
    if not new_netflix_gcs:
        errors.append(
            "No new $30 Netflix gift card found (should match most recently purchased active card)."
        )
    else:
        gc = new_netflix_gcs[0]
        user_email = state.get("currentUser", {}).get("email", "")
        if gc.get("recipientEmail") != user_email:
            errors.append(
                f"Netflix gift card recipient is '{gc.get('recipientEmail')}', "
                f"expected '{user_email}' (self)."
            )

    # Should have a gift_card transaction for Netflix
    transactions = state.get("transactions", [])
    found_gc_txn = any(
        t.get("type") == "gift_card" and "Netflix" in (t.get("description") or "")
        and t.get("amount") == -30
        for t in transactions
    )
    if not found_gc_txn:
        errors.append("No gift_card transaction for $30 Netflix found.")

    if errors:
        return False, " ".join(errors)
    return True, "Bought $30 Netflix gift card for self (matching most recently purchased active card)."
