import requests


def verify(server_url: str) -> tuple[bool, str]:
    """Favorites overhaul + settings: remove antibiotics, add Gabapentin/Diclofenac, update settings."""
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."

    state = resp.json()
    errors = []
    settings = state.get("settings", {})
    favs = settings.get("favoritesDrugIds", [])

    # Antibiotics removed
    if "drug_025" in favs:
        errors.append("Amoxicillin (drug_025) is still in favorites.")
    if "drug_028" in favs:
        errors.append("Azithromycin (drug_028) is still in favorites.")

    # Gabapentin and Diclofenac added
    if "drug_036" not in favs:
        errors.append("Gabapentin (drug_036) not found in favorites.")
    if "drug_044" not in favs:
        errors.append("Diclofenac (drug_044) not found in favorites.")

    # Settings
    if settings.get("defaultDaysSupply") != 14:
        errors.append(f"Expected defaultDaysSupply 14, got {settings.get('defaultDaysSupply')}.")
    if settings.get("printFormat") != "detailed":
        errors.append(f"Expected printFormat 'detailed', got '{settings.get('printFormat')}'.")

    if errors:
        return False, " ".join(errors)
    return True, "Favorites updated and settings changed correctly."
