import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()

    errors = []

    # Check Chainlink quantity decreased (sold $200 worth)
    crypto_holdings = state.get("cryptoHoldings", [])
    link = None
    for c in crypto_holdings:
        if c.get("symbol") == "LINK":
            link = c
            break

    if link is None:
        errors.append("Chainlink not found in crypto holdings.")
    else:
        # Seed quantity was 12.5. After selling $200 worth, it should be less.
        if link.get("quantity", 12.5) >= 12.49:
            errors.append(
                f"Chainlink quantity is {link.get('quantity')}, expected it to decrease "
                f"from 12.5 after selling $200 worth."
            )

    # Check a crypto_sell transaction for Chainlink exists
    transactions = state.get("transactions", [])
    found_sell = False
    for t in transactions:
        if t.get("type") == "crypto_sell":
            desc = (t.get("description") or "").lower()
            if "chainlink" in desc:
                found_sell = True
                break
    if not found_sell:
        errors.append("No crypto_sell transaction for Chainlink found.")

    # Check savings balance increased from 12450.82
    savings = state.get("savingsAccount")
    if savings is None:
        errors.append("No savingsAccount found in state.")
    else:
        if savings.get("balance", 0) <= 12450.82:
            errors.append(
                f"Savings balance is {savings.get('balance')}, expected > 12450.82 "
                f"after depositing $200."
            )
        # Check for a new savings deposit entry
        transfer_history = savings.get("transferHistory", [])
        seed_ids = {"stx_001", "stx_002", "stx_003", "stx_004", "stx_005", "stx_006", "stx_007", "stx_008"}
        found_deposit = False
        for entry in transfer_history:
            if entry.get("type") == "deposit" and entry.get("id") not in seed_ids:
                found_deposit = True
                break
        if not found_deposit:
            errors.append("No new deposit entry found in savings transferHistory.")

    if errors:
        return False, " ".join(errors)
    return True, "Successfully sold $200 of Chainlink and deposited $200 into savings."
