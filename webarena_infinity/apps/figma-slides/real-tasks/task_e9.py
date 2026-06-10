import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, f"Failed to fetch state: HTTP {resp.status_code}"
    state = resp.json()

    deck_settings = state.get("deckSettings", {})
    available_offline = deck_settings.get("availableOffline")

    if available_offline is not True:
        return False, f"availableOffline is {available_offline}, expected True"

    return True, "Deck is now available offline"
