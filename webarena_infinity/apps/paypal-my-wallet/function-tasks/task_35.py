import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()

    offers = state.get("offers", [])
    if not offers:
        return False, "No offers found in state."

    for offer in offers:
        if offer.get("merchantName") == "Starbucks":
            status = offer.get("status")
            saved_at = offer.get("savedAt")
            if status == "available" and saved_at is None:
                return True, "Starbucks offer successfully unsaved."
            errors = []
            if status != "available":
                errors.append(f"Expected status 'available', got '{status}'.")
            if saved_at is not None:
                errors.append(f"Expected savedAt to be None, but got '{saved_at}'.")
            return False, f"Starbucks offer found but not properly unsaved. " + " ".join(errors)

    return False, "Starbucks offer not found in offers list."
