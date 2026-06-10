import requests


def verify(server_url: str) -> tuple[bool, str]:
    try:
        resp = requests.get(f"{server_url}/api/state")
        if resp.status_code != 200:
            return False, f"Failed to fetch state: HTTP {resp.status_code}"
        state = resp.json()
    except Exception as e:
        return False, f"Error fetching state: {e}"

    allergies = state.get("currentPatient", {}).get("allergies", [])
    allergen_names = [a.get("allergen", "").lower() for a in allergies]

    # Penicillin should be removed
    if "penicillin" in allergen_names:
        return False, "Penicillin allergy still present, should have been removed"

    # Codeine should be removed
    if "codeine" in allergen_names:
        return False, "Codeine allergy still present, should have been removed"

    # Erythromycin should be added
    erythromycin = None
    for a in allergies:
        if "erythromycin" in a.get("allergen", "").lower():
            erythromycin = a
            break
    if erythromycin is None:
        return False, "Erythromycin allergy not found"
    if erythromycin.get("severity") != "Severe":
        return False, f"Erythromycin severity is '{erythromycin.get('severity')}', expected 'Severe'"
    reaction = erythromycin.get("reaction", "").lower()
    if "qt" not in reaction and "prolongation" not in reaction:
        return False, f"Erythromycin reaction should mention QT prolongation, got: '{erythromycin.get('reaction')}'"
    if erythromycin.get("type") != "drug":
        return False, f"Erythromycin type is '{erythromycin.get('type')}', expected 'drug'"

    # Sulfonamides and Latex should still be present (unchanged)
    if "sulfonamides" not in allergen_names:
        return False, "Sulfonamides allergy was removed but should remain"

    return True, "Penicillin and Codeine allergies removed, Erythromycin allergy added"
