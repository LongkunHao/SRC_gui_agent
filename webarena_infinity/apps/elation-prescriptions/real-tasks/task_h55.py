import requests


def verify(server_url: str) -> tuple[bool, str]:
    try:
        resp = requests.get(f"{server_url}/api/state")
        if resp.status_code != 200:
            return False, f"Failed to fetch state: HTTP {resp.status_code}"
        state = resp.json()
    except Exception as e:
        return False, f"Error fetching state: {e}"

    # Check Morphine allergy added
    allergies = state.get("currentPatient", {}).get("allergies", [])
    morphine_allergy = None
    for a in allergies:
        if "morphine" in a.get("allergen", "").lower():
            morphine_allergy = a
            break
    if morphine_allergy is None:
        return False, "Morphine allergy not found"
    if morphine_allergy.get("severity") != "Severe":
        return False, f"Morphine allergy severity is '{morphine_allergy.get('severity')}', expected 'Severe'"
    reaction = morphine_allergy.get("reaction", "").lower()
    if "respiratory" not in reaction and "depression" not in reaction:
        return False, f"Morphine reaction should mention respiratory depression, got: '{morphine_allergy.get('reaction')}'"

    # Check drug-to-allergy alerts disabled
    settings = state.get("settings", {})
    dds = settings.get("drugDecisionSupport", {})
    if dds.get("drugToAllergyEnabled") is not False:
        return False, "Drug-to-allergy alerts should be disabled"

    # Check drug interaction level set to major_only
    if dds.get("drugToDrugLevel") != "major_only":
        return False, f"Drug interaction level is '{dds.get('drugToDrugLevel')}', expected 'major_only'"

    return True, "Morphine allergy added, allergy alerts disabled, interactions set to Major only"
