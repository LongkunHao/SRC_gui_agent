import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()

    errors = []

    # Custom auto labels: Team Update (al_6), Investor (al_7), Support Ticket (al_8)
    # All should be disabled
    for al in state.get("autoLabels", []):
        if al.get("type") == "custom" and al.get("enabled"):
            errors.append(f"Custom auto label '{al['name']}' is still enabled.")

    # Shipping Update (al_5, library) should be enabled
    shipping = None
    for al in state.get("autoLabels", []):
        if al.get("name") == "Shipping Update":
            shipping = al
            break

    if not shipping:
        return False, "Shipping Update auto label not found."

    if not shipping.get("enabled"):
        errors.append("Shipping Update auto label is not enabled.")

    if errors:
        return False, " ".join(errors)

    return True, "All custom auto labels disabled and Shipping Update enabled."
