import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()

    errors = []

    # No card should have status 'pending_confirmation'
    cards = state.get("cards", [])
    pending_cards = [c for c in cards if c.get("status") == "pending_confirmation"]
    if pending_cards:
        names = [f"{c.get('brand')} {c.get('lastFour')}" for c in pending_cards]
        errors.append(
            f"Found {len(pending_cards)} unconfirmed card(s) still present: {', '.join(names)}."
        )

    # No bank account should have status 'pending_confirmation'
    banks = state.get("bankAccounts", [])
    pending_banks = [b for b in banks if b.get("status") == "pending_confirmation"]
    if pending_banks:
        names = [f"{b.get('bankName')} {b.get('lastFour')}" for b in pending_banks]
        errors.append(
            f"Found {len(pending_banks)} unconfirmed bank account(s) still present: {', '.join(names)}."
        )

    # Verify that confirmed methods are still there
    confirmed_cards = [c for c in cards if c.get("status") == "confirmed"]
    if len(confirmed_cards) < 4:
        errors.append(
            f"Expected at least 4 confirmed cards to remain, found {len(confirmed_cards)}."
        )

    confirmed_banks = [b for b in banks if b.get("status") == "confirmed"]
    if len(confirmed_banks) < 4:
        errors.append(
            f"Expected at least 4 confirmed bank accounts to remain, found {len(confirmed_banks)}."
        )

    if errors:
        return False, " ".join(errors)
    return True, "All unconfirmed payment methods have been removed."
