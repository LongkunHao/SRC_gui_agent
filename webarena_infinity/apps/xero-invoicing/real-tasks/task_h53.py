import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."

    state = resp.json()
    themes = state.get("brandingThemes", [])
    theme_names = [t.get("name", "") for t in themes]

    errors = []

    # Simple Clean should be deleted
    if any("Simple Clean" in n for n in theme_names):
        errors.append("Simple Clean theme should be deleted.")

    # Retail should be deleted
    if any(n == "Retail" for n in theme_names):
        errors.append("Retail theme should be deleted.")

    # Modern theme should exist with showPaymentAdvice=false
    modern = next((t for t in themes if t.get("name") == "Modern"), None)
    if modern is None:
        errors.append("'Modern' branding theme not found.")
    else:
        if modern.get("showPaymentAdvice") is not False:
            errors.append(f"'Modern' should have showPaymentAdvice=false, got {modern.get('showPaymentAdvice')}.")

    if errors:
        return False, " ".join(errors)

    return True, "Simple Clean and Retail deleted, 'Modern' theme created with payment advice disabled."
