import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."

    state = resp.json()
    themes = state.get("brandingThemes", [])

    # Find 'Minimal' theme
    minimal = next((t for t in themes if t.get("name") == "Minimal"), None)
    if minimal is None:
        return False, "Branding theme 'Minimal' not found."

    if minimal.get("showTaxNumber") is not False:
        return False, f"Expected showTaxNumber=False on Minimal theme, got {minimal.get('showTaxNumber')}."

    if minimal.get("showPaymentAdvice") is not False:
        return False, f"Expected showPaymentAdvice=False on Minimal theme, got {minimal.get('showPaymentAdvice')}."

    if minimal.get("isDefault") is not True:
        return False, "Expected Minimal theme to be the default."

    # No other theme should be default
    other_defaults = [t for t in themes if t.get("isDefault") and t.get("name") != "Minimal"]
    if other_defaults:
        return False, f"Other themes still marked as default: {[t['name'] for t in other_defaults]}"

    return True, "Branding theme 'Minimal' created, tax number and payment advice disabled, set as default."
