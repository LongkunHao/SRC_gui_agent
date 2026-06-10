import requests


def verify(server_url: str) -> tuple[bool, str]:
    try:
        resp = requests.get(f"{server_url}/api/state")
        if resp.status_code != 200:
            return False, f"Failed to fetch state: HTTP {resp.status_code}"
        state = resp.json()
    except Exception as e:
        return False, f"Error fetching state: {e}"

    # Check Tramadol allergy was added
    allergies = state.get("currentPatient", {}).get("allergies", [])
    tramadol_allergy = None
    for allergy in allergies:
        if "tramadol" in allergy.get("allergen", "").lower():
            tramadol_allergy = allergy
            break
    if tramadol_allergy is None:
        return False, "Tramadol allergy not found in patient allergies"

    severity = tramadol_allergy.get("severity", "").lower()
    if severity != "severe":
        return False, f"Tramadol allergy severity is '{tramadol_allergy.get('severity')}', expected 'Severe'"

    reaction = tramadol_allergy.get("reaction", "").lower()
    if "seizure" not in reaction:
        return False, f"Tramadol allergy reaction is '{tramadol_allergy.get('reaction')}', expected to mention seizures"

    allergy_type = tramadol_allergy.get("type", "").lower()
    if allergy_type != "drug":
        return False, f"Tramadol allergy type is '{tramadol_allergy.get('type')}', expected 'drug'"

    # Check drug interaction alerts set to Major only
    settings = state.get("settings", {})
    dds = settings.get("drugDecisionSupport", {})
    level = dds.get("drugToDrugLevel")
    if level != "major_only":
        return False, f"Drug interaction alert level is '{level}', expected 'major_only'"

    return True, "Tramadol allergy added (Severe, seizures) and drug interaction alerts set to Major only"
