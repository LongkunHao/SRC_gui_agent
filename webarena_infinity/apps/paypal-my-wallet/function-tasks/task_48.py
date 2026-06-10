import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()

    prefs = state.get("walletPreferences", {})
    currency_option = prefs.get("currencyConversionOption", "")

    if currency_option != "card_issuer":
        return False, f"Expected walletPreferences.currencyConversionOption to be 'card_issuer', got '{currency_option}'."

    return True, "Currency conversion option successfully set to 'card_issuer'."
