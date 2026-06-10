import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()

    errors = []

    cards = state.get("cards", [])

    # Preferred credit card is Visa 4829 (card_001) — should be kept.
    # Backup is Mastercard 2290 (card_006) — should be kept.
    # American Express 3001 (card_003) — should be removed (credit, not preferred/backup).
    # Discover 6221 (card_004) — should be removed (credit, expired, not preferred/backup).
    # Debit cards (7156, 8834) should NOT be removed (they're debit, not credit).

    remaining_last_fours = {c.get("lastFour") for c in cards}

    # Cards that should be removed
    for lf in ["3001", "6221"]:
        if lf in remaining_last_fours:
            errors.append(f"Credit card ending in {lf} should have been removed.")

    # Cards that should remain
    for lf in ["4829", "2290"]:
        if lf not in remaining_last_fours:
            errors.append(f"Card ending in {lf} was removed but should have been kept (preferred or backup).")

    # Debit cards should remain untouched
    for lf in ["7156", "8834"]:
        if lf not in remaining_last_fours:
            errors.append(f"Debit card ending in {lf} was removed but should not have been (not a credit card).")

    if errors:
        return False, " ".join(errors)
    return True, "Removed all credit cards not set as preferred or backup."
