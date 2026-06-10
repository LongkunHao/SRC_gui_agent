import requests


def verify(server_url: str) -> tuple[bool, str]:
    """Clinic policy settings: generic first on, auto-interactions on, allergy review off, Safeway default."""
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."

    state = resp.json()
    errors = []
    settings = state.get("settings", {})

    if settings.get("showGenericFirst") is not True:
        errors.append(f"Expected showGenericFirst True, got {settings.get('showGenericFirst')}.")
    if settings.get("autoCheckInteractions") is not True:
        errors.append(f"Expected autoCheckInteractions True, got {settings.get('autoCheckInteractions')}.")
    if settings.get("requireAllergyReview") is not False:
        errors.append(f"Expected requireAllergyReview False, got {settings.get('requireAllergyReview')}.")
    if settings.get("defaultPharmacy") != "pharm_012":
        errors.append(f"Expected defaultPharmacy 'pharm_012' (Safeway), got '{settings.get('defaultPharmacy')}'.")

    if errors:
        return False, " ".join(errors)
    return True, "Clinic policy settings applied correctly."
