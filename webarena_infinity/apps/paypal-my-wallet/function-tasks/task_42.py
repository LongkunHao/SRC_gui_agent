import requests


SEED_USD_BALANCE = 2847.63
GIFT_CARD_AMOUNT = 50
SEED_GIFT_CARD_COUNT = 5


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()

    errors = []

    # Check for the new Amazon gift card
    gift_cards = state.get("giftCards", [])
    found_card = None
    for gc in gift_cards:
        if (
            gc.get("merchantName") == "Amazon"
            and gc.get("amount") == GIFT_CARD_AMOUNT
            and gc.get("recipientEmail") == "alex.johnson@email.com"
        ):
            found_card = gc
            break

    if not found_card:
        errors.append(
            "No gift card found with merchantName=='Amazon', amount==50, and recipientEmail=='alex.johnson@email.com'."
        )
    else:
        if found_card.get("recipientName") != "Alex Johnson":
            errors.append(
                f"Expected recipientName 'Alex Johnson', got '{found_card.get('recipientName')}'."
            )
        if found_card.get("message") != "Happy Birthday!":
            errors.append(
                f"Expected message 'Happy Birthday!', got '{found_card.get('message')}'."
            )
        if found_card.get("status") != "active":
            errors.append(
                f"Expected status 'active', got '{found_card.get('status')}'."
            )

    # Check USD balance decreased by $50
    balances = state.get("balances", [])
    usd_balance = None
    for b in balances:
        if b.get("currency") == "USD":
            usd_balance = b.get("amount")
            break
    if usd_balance is None:
        usd_balance = state.get("balance", {}).get("amount") if isinstance(state.get("balance"), dict) else state.get("balance")

    if usd_balance is not None:
        expected_usd = SEED_USD_BALANCE - GIFT_CARD_AMOUNT
        if abs(usd_balance - expected_usd) > 0.01:
            errors.append(
                f"Expected USD balance around {expected_usd}, got {usd_balance}."
            )
    else:
        errors.append("Could not find USD balance in state.")

    # Check for a gift_card transaction
    transactions = state.get("transactions", [])
    found_transaction = False
    for txn in transactions:
        txn_type = txn.get("type", "")
        txn_desc = txn.get("description", "") or txn.get("name", "") or txn.get("merchant", "") or ""
        if txn_type == "gift_card" and "Amazon" in txn_desc:
            found_transaction = True
            break

    if not found_transaction:
        errors.append(
            "No transaction found with type=='gift_card' containing 'Amazon' in description."
        )

    if errors:
        return False, " ".join(errors)
    return True, "Successfully purchased $50 Amazon gift card for alex.johnson@email.com. Gift card created, USD balance decreased, and transaction recorded."
