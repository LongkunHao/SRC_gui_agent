import requests


def verify(server_url: str) -> tuple[bool, str]:
    """Remove NSAIDs + corticosteroids from favorites, update settings, renew Albuterol."""
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."

    state = resp.json()
    errors = []

    favs = state.get("settings", {}).get("favoritesDrugIds", [])
    # Ibuprofen (NSAID) removed
    if "drug_043" in favs:
        errors.append("Ibuprofen (drug_043, NSAID) still in favorites.")
    # Prednisone (corticosteroid) removed
    if "drug_045" in favs:
        errors.append("Prednisone (drug_045, corticosteroid) still in favorites.")

    # Settings
    settings = state.get("settings", {})
    if settings.get("defaultDaysSupply") != 60:
        errors.append(f"Expected defaultDaysSupply 60, got {settings.get('defaultDaysSupply')}.")
    if settings.get("defaultRefills") != 2:
        errors.append(f"Expected defaultRefills 2, got {settings.get('defaultRefills')}.")

    # rx_006 (Albuterol) renewed with 5 refills
    rx_006 = next((r for r in state["prescriptions"] if r["id"] == "rx_006"), None)
    if not rx_006:
        errors.append("Prescription rx_006 (Albuterol) not found.")
    elif rx_006.get("refillsRemaining", 0) < 5:
        errors.append(f"Expected rx_006 (Albuterol) refillsRemaining >= 5, got {rx_006.get('refillsRemaining')}.")

    if errors:
        return False, " ".join(errors)
    return True, "Favorites cleaned, settings updated, Albuterol renewed."
