import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."

    state = resp.json()
    settings = state.get("settings", {})
    favorites = settings.get("favoritesDrugIds", [])

    if "drug_034" not in favorites:
        return False, f"Expected 'drug_034' (Escitalopram) in settings.favoritesDrugIds, but it was not found. Current favorites: {favorites}."

    return True, "Escitalopram (drug_034) added to the favorites list."
