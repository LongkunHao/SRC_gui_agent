import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, f"Failed to fetch state: HTTP {resp.status_code}"
    state = resp.json()

    deck_settings = state.get("deckSettings", {})
    name = deck_settings.get("name")

    if name != "Q4 2025 Strategy Update":
        return False, f"Deck name is '{name}', expected 'Q4 2025 Strategy Update'"

    return True, "Presentation renamed to 'Q4 2025 Strategy Update'"
