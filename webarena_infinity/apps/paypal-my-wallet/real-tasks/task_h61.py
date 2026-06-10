import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()

    errors = []

    # Chainlink should have 0 (or near-zero) quantity after selling all
    link = None
    for c in state.get("cryptoHoldings", []):
        if c.get("symbol") == "LINK":
            link = c
            break

    if link is None:
        errors.append("Chainlink not found in crypto holdings.")
    else:
        if link.get("quantity", 1) > 0.001:
            errors.append(
                f"Chainlink quantity is {link.get('quantity')}, expected ~0 after selling all holdings."
            )

    # Savings should have increased by $200 (from 12450.82 to ~12650.82)
    savings = state.get("savingsAccount")
    if savings is None:
        errors.append("Savings account not found.")
    else:
        expected_savings = 12450.82 + 200
        if abs(savings.get("balance", 0) - expected_savings) > 1.0:
            errors.append(
                f"Savings balance is {savings.get('balance')}, expected ~{expected_savings} "
                f"after depositing $200."
            )

    # Should have a crypto_sell transaction for Chainlink
    transactions = state.get("transactions", [])
    found_sell = any(
        t.get("type") == "crypto_sell" and "Chainlink" in (t.get("description") or "")
        for t in transactions
    )
    if not found_sell:
        errors.append("No crypto_sell transaction for Chainlink found.")

    if errors:
        return False, " ".join(errors)
    return True, "Sold all Chainlink holdings and deposited $200 into savings."
