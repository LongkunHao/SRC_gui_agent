import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."

    state = resp.json()
    themes = state.get("brandingThemes", [])

    errors = []
    for t in themes:
        name = t.get("name", "")
        if not t.get("showTaxNumber"):
            errors.append(f"'{name}' should have showTaxNumber=true.")

    # Standard and Professional originally had showPaymentAdvice=true → should now be false
    # Simple Clean and Retail originally had showPaymentAdvice=false → should remain false
    for t in themes:
        name = t.get("name", "")
        if t.get("showPaymentAdvice"):
            errors.append(f"'{name}' should have showPaymentAdvice=false (was true in seed or should stay false).")

    if errors:
        return False, " ".join(errors)

    return True, "All themes: tax number enabled, payment advice disabled on those that had it."
