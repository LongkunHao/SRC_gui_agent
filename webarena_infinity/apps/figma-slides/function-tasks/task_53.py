import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()

    deck_settings = state.get("deckSettings", {})
    name = deck_settings.get("name")
    expected = "Q4 2025 Product Strategy & Roadmap"

    if name == expected:
        return True, f"Deck name is correctly '{expected}'."
    else:
        return False, f"Deck name is '{name}', expected '{expected}'."
