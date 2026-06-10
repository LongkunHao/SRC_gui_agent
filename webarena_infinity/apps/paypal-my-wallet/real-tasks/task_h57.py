import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()

    errors = []

    # Check for new DoorDash gift card for self ($25)
    gift_cards = state.get("giftCards", [])
    seed_gc_ids = {"gc_001", "gc_002", "gc_003", "gc_004", "gc_005"}
    found_gc = False
    for gc in gift_cards:
        if gc.get("id") not in seed_gc_ids:
            if gc.get("merchantName") == "DoorDash" and gc.get("amount") == 25:
                user = state.get("currentUser", {})
                if gc.get("recipientEmail") == user.get("email"):
                    found_gc = True
                    break
    if not found_gc:
        errors.append("No new $25 DoorDash gift card for self found.")

    # Check LTC quantity decreased (from seed 5.234)
    crypto_holdings = state.get("cryptoHoldings", [])
    ltc = None
    for c in crypto_holdings:
        if c.get("symbol") == "LTC":
            ltc = c
            break

    if ltc is None:
        errors.append("Litecoin not found in crypto holdings.")
    else:
        seed_quantity = 5.234
        if ltc.get("quantity", 0) >= seed_quantity:
            errors.append(
                f"Litecoin quantity is {ltc.get('quantity')}, expected < {seed_quantity} "
                f"after selling $25."
            )

        # Check for sell transaction
        ltc_txns = ltc.get("transactions", [])
        seed_tx_ids = {"ctx_008", "ctx_009"}
        found_sell = False
        for tx in ltc_txns:
            if tx.get("type") == "sell" and tx.get("id") not in seed_tx_ids:
                found_sell = True
                break
        if not found_sell:
            errors.append("No new sell transaction found in Litecoin's transaction history.")

    if errors:
        return False, " ".join(errors)
    return True, "Bought $25 DoorDash gift card for self and sold $25 of Litecoin."
