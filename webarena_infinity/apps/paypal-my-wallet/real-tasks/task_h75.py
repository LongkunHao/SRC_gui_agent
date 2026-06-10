import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()

    errors = []

    # Step 1: Savings should have decreased by $1,500 (from 12450.82 to ~10950.82)
    savings = state.get("savingsAccount")
    if savings is None:
        errors.append("Savings account not found.")
    else:
        expected_savings = 12450.82 - 1500
        if abs(savings.get("balance", 0) - expected_savings) > 1.0:
            errors.append(
                f"Savings balance is {savings.get('balance')}, expected ~{expected_savings} "
                f"after withdrawing $1,500."
            )

    balances = state.get("balances", [])
    transactions = state.get("transactions", [])

    # Step 2: Should have a transfer_in from Chase
    found_transfer_in = any(
        t.get("type") == "transfer_in"
        and "Chase" in (t.get("description") or "")
        and t.get("amount") == 500
        for t in transactions
    )
    if not found_transfer_in:
        errors.append("No transfer_in of $500 from Chase found.")

    # Step 3: EUR balance should have increased (from seed 523.18)
    eur_bal = None
    for b in balances:
        if b.get("currency") == "EUR":
            eur_bal = b
            break

    if eur_bal is None:
        errors.append("EUR balance not found.")
    else:
        seed_eur = 523.18
        if eur_bal.get("amount", 0) <= seed_eur:
            errors.append(
                f"EUR balance is {eur_bal.get('amount')}, expected > {seed_eur} "
                f"after converting $1,000."
            )

    # Step 4: Should have a new $100 Best Buy gift card for self
    gift_cards = state.get("giftCards", [])
    seed_gc_ids = {"gc_001", "gc_002", "gc_003", "gc_004", "gc_005"}
    new_bb_gcs = [
        gc for gc in gift_cards
        if gc.get("id") not in seed_gc_ids
        and gc.get("merchantName") == "Best Buy"
        and gc.get("amount") == 100
    ]
    if not new_bb_gcs:
        errors.append("No new $100 Best Buy gift card found.")
    else:
        gc = new_bb_gcs[0]
        user_email = state.get("currentUser", {}).get("email", "")
        if gc.get("recipientEmail") != user_email:
            errors.append(
                f"Best Buy gift card recipient is '{gc.get('recipientEmail')}', "
                f"expected '{user_email}' (self)."
            )

    if errors:
        return False, " ".join(errors)
    return True, "Withdrew $1,500 from savings, added $500 from Chase, converted $1,000 to EUR, bought $100 Best Buy gift card."
