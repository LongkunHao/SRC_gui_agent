import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()

    cards = state.get("cards", [])

    for card in cards:
        if card.get("lastFour") == "6221":
            return False, "Expired Discover card ****6221 still exists in cards."

    return True, "Expired Discover card ****6221 has been removed."
