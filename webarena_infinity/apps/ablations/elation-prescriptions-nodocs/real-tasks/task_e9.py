import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."

    state = resp.json()

    settings = state.get("settings", {})
    favorites = settings.get("favoritesDrugIds", [])

    if "drug_045" in favorites:
        return False, "Prednisone (drug_045) is still in the favoritesDrugIds list."

    return True, "Prednisone (drug_045) has been removed from prescription favorites."
