import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()

    # Check gift cards
    gift_cards = state.get("giftCards", [])
    if not isinstance(gift_cards, list):
        return False, f"Expected giftCards to be a list, got {type(gift_cards).__name__}."

    # Total gift cards should have increased by 1 (seed had 5)
    if len(gift_cards) < 6:
        return False, f"Expected at least 6 gift cards (5 seed + 1 new), found {len(gift_cards)}."

    # Find the Starbucks gift card
    starbucks_cards = [
        gc for gc in gift_cards
        if gc.get("merchantName", "").lower() == "starbucks"
        and gc.get("amount") in (25, 25.0, "25", "$25", "$25.00")
    ]
    if not starbucks_cards:
        return False, "No Starbucks gift card with amount $25 found."

    card = starbucks_cards[0]

    # Check amount is 25
    amount = card.get("amount")
    if isinstance(amount, str):
        amount = float(amount.replace("$", "").replace(",", ""))
    if amount != 25:
        return False, f"Expected Starbucks gift card amount to be 25, got {amount}."

    # Check recipientEmail
    recipient_email = card.get("recipientEmail", "")
    if recipient_email.lower() != "jordan.mitchell@outlook.com":
        return False, f"Expected recipientEmail 'jordan.mitchell@outlook.com', got '{recipient_email}'."

    # Check recipientName
    recipient_name = card.get("recipientName", "")
    if recipient_name.lower() != "jordan mitchell":
        return False, f"Expected recipientName 'Jordan Mitchell', got '{recipient_name}'."

    # Check status
    status = card.get("status", "")
    if status != "active":
        return False, f"Expected gift card status 'active', got '{status}'."

    # Check USD balance decreased by $25 (seed was 2847.63, should be ~2822.63)
    balance = state.get("balance", {})
    if isinstance(balance, dict):
        usd_balance = balance.get("USD", balance.get("usd", None))
        if usd_balance is None:
            # Try currencies list
            currencies = balance.get("currencies", [])
            for c in currencies:
                if c.get("code", "").upper() == "USD" or c.get("currency", "").upper() == "USD":
                    usd_balance = c.get("amount", c.get("balance", c.get("value")))
                    break
    elif isinstance(balance, (int, float)):
        usd_balance = balance
    else:
        usd_balance = None

    if usd_balance is not None:
        if isinstance(usd_balance, str):
            usd_balance = float(usd_balance.replace("$", "").replace(",", ""))
        expected_balance = 2847.63 - 25
        if abs(float(usd_balance) - expected_balance) > 0.01:
            return False, f"Expected USD balance ~{expected_balance} after $25 purchase, got {usd_balance}."

    return True, "Starbucks $25 gift card purchased successfully for self with correct details."
