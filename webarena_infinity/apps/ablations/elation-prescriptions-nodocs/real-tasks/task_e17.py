import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."

    state = resp.json()

    settings = state.get("settings", {})
    favorites = settings.get("favoritesDrugIds", [])

    if "drug_043" in favorites:
        return False, "Ibuprofen (drug_043) is still in the favoritesDrugIds list."

    return True, "Ibuprofen (drug_043) has been removed from formulary favorites."
