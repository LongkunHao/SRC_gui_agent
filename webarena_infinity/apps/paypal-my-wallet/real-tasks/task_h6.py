import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()

    errors = []

    # Check that Discover card ending in 6221 (card_004, expired) has been removed
    cards = state.get("cards", [])
    for c in cards:
        if c.get("lastFour") == "6221":
            errors.append("Expired Discover card ending in 6221 is still present in cards.")
            break

    # Check that Wells Fargo bank ending in 5518 (bank_003, pending) has been removed
    bank_accounts = state.get("bankAccounts", [])
    for b in bank_accounts:
        if b.get("lastFour") == "5518":
            errors.append("Unconfirmed Wells Fargo account ending in 5518 is still present in bankAccounts.")
            break

    if errors:
        return False, " ".join(errors)
    return True, "Expired Discover card (6221) and unconfirmed Wells Fargo account (5518) have been removed."
