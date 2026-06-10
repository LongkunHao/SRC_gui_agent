import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()

    deck_settings = state.get("deckSettings", {})
    available_offline = deck_settings.get("availableOffline")

    if available_offline is True:
        return True, "deckSettings.availableOffline is correctly set to True."
    else:
        return False, f"deckSettings.availableOffline is {available_offline}, expected True."
