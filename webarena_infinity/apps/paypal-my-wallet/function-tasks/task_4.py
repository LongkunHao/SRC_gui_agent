import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()

    cards = state.get("cards", [])

    target = None
    for card in cards:
        if card.get("lastFour") == "8834":
            target = card
            break

    if target is None:
        return False, "Card with lastFour '8834' not found in cards."

    if target.get("status") != "confirmed":
        return False, f"Card ****8834 status is '{target.get('status')}', expected 'confirmed'."

    if target.get("confirmedAt") is None:
        return False, "Card ****8834 confirmedAt is None, expected a timestamp."

    return True, "Visa ****8834 has been confirmed successfully."
