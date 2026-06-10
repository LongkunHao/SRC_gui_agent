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
        if offer.get("merchantName") == "Target":
            status = offer.get("status")
            saved_at = offer.get("savedAt")
            if status == "saved" and saved_at is not None:
                return True, "Target offer successfully saved."
            errors = []
            if status != "saved":
                errors.append(f"Expected status 'saved', got '{status}'.")
            if saved_at is None:
                errors.append("Expected savedAt to be set, but it is None.")
            return False, f"Target offer found but not properly saved. " + " ".join(errors)

    return False, "Target offer not found in offers list."
