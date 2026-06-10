import requests


def verify(server_url: str) -> tuple[bool, str]:
    try:
        resp = requests.get(f"{server_url}/api/state")
        if resp.status_code != 200:
            return False, f"Failed to fetch state: HTTP {resp.status_code}"
        state = resp.json()
    except Exception as e:
        return False, f"Error fetching state: {e}"

    # Check Penicillin allergy removed
    allergies = state.get("currentPatient", {}).get("allergies", [])
    for allergy in allergies:
        if allergy.get("allergen", "").lower() == "penicillin":
            return False, "Penicillin allergy still present in patient allergies"

    # Check Amoxicillin 875mg prescribed as temporary
    temporary = state.get("temporaryMeds", [])
    amoxicillin = None
    for med in temporary:
        name = med.get("medicationName", "").lower()
        if "amoxicillin" in name and "875mg" in name:
            amoxicillin = med
            break
    if amoxicillin is None:
        # Also check permanentRxMeds in case agent classified differently
        for med in state.get("permanentRxMeds", []):
            name = med.get("medicationName", "").lower()
            if "amoxicillin" in name and "875mg" in name:
                return False, "Amoxicillin 875mg found in permanentRxMeds but should be temporary"
        return False, "No Amoxicillin 875mg found in temporaryMeds"

    qty = amoxicillin.get("qty")
    if qty != 20:
        return False, f"Amoxicillin 875mg qty is {qty}, expected 20"

    refills = amoxicillin.get("refills", amoxicillin.get("refillsRemaining"))
    if refills != 0:
        return False, f"Amoxicillin 875mg refills is {refills}, expected 0"

    days = amoxicillin.get("daysSupply")
    if days != 10:
        return False, f"Amoxicillin 875mg daysSupply is {days}, expected 10"

    pharmacy_id = amoxicillin.get("pharmacyId", "")
    pharmacy_name = amoxicillin.get("pharmacyName", "")
    if pharmacy_id != "pharm_001" and "cvs" not in pharmacy_name.lower():
        return False, f"Amoxicillin pharmacy is '{pharmacy_name}' ({pharmacy_id}), expected CVS #4521"

    return True, "Penicillin allergy removed, Amoxicillin 875mg prescribed as temporary to CVS"
