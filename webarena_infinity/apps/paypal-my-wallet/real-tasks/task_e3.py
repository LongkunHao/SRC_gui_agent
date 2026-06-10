import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()

    offers = state.get("offers")
    if offers is None:
        return False, "No offers found in state."

    doordash_offers = [o for o in offers if o.get("merchantName") == "DoorDash"]
    if not doordash_offers:
        return False, "No DoorDash offer found in state."

    for offer in doordash_offers:
        if offer.get("status") == "saved":
            return True, "DoorDash cashback deal has been successfully saved."

    current_statuses = [o.get("status") for o in doordash_offers]
    return False, f"DoorDash offer is not saved. Current status(es): {current_statuses}."
