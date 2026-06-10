import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()

    cards = state.get("cards", [])

    target = None
    for card in cards:
        if card.get("lastFour") == "3001":
            target = card
            break

    if target is None:
        return False, "Card with lastFour '3001' not found in cards."

    billing = target.get("billingAddress", {})
    if not billing:
        return False, "Card ****3001 has no billingAddress."

    errors = []
    if billing.get("street") != "100 Market St":
        errors.append(f"street is '{billing.get('street')}', expected '100 Market St'")
    if billing.get("city") != "San Jose":
        errors.append(f"city is '{billing.get('city')}', expected 'San Jose'")
    if billing.get("state") != "CA":
        errors.append(f"state is '{billing.get('state')}', expected 'CA'")
    if billing.get("zip") != "95110":
        errors.append(f"zip is '{billing.get('zip')}', expected '95110'")
    if billing.get("country") != "US":
        errors.append(f"country is '{billing.get('country')}', expected 'US'")

    if errors:
        return False, "Billing address mismatch for card ****3001: " + "; ".join(errors)

    return True, "Amex ****3001 billing address updated to 100 Market St, San Jose, CA 95110, US."
