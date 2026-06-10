import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()

    cards = state.get("cards", [])

    if len(cards) != 7:
        return False, f"Expected 7 cards after adding new card, found {len(cards)}."

    new_card = None
    for card in cards:
        if card.get("lastFour") == "9999":
            new_card = card
            break

    if new_card is None:
        return False, "No card with lastFour '9999' found in cards."

    if new_card.get("brand") != "Visa":
        return False, f"New card brand is '{new_card.get('brand')}', expected 'Visa'."

    if new_card.get("type") != "credit":
        return False, f"New card type is '{new_card.get('type')}', expected 'credit'."

    if new_card.get("status") != "pending_confirmation":
        return False, f"New card status is '{new_card.get('status')}', expected 'pending_confirmation'."

    return True, "New Visa credit card ****9999 has been added successfully."
