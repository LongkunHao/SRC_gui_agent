import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()

    prefs = state.get("walletPreferences")
    if prefs is None:
        return False, "No wallet preferences found in state."

    conversion_option = prefs.get("currencyConversionOption")
    if conversion_option != "card_issuer":
        return False, f"Currency conversion option is '{conversion_option}', expected 'card_issuer'."

    return True, "Currency conversion option has been successfully set to card issuer."
