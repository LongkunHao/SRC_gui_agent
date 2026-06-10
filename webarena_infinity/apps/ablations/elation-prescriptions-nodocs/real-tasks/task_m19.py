import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."

    state = resp.json()
    settings = state.get("settings", {})
    favorites = settings.get("favoritesDrugIds", [])

    errors = []

    if "drug_025" in favorites:
        errors.append("drug_025 (Amoxicillin) is still in favoritesDrugIds.")

    if "drug_028" in favorites:
        errors.append("drug_028 (Azithromycin) is still in favoritesDrugIds.")

    if errors:
        return False, " ".join(errors)

    return True, "Both Amoxicillin (drug_025) and Azithromycin (drug_028) removed from formulary favorites."
