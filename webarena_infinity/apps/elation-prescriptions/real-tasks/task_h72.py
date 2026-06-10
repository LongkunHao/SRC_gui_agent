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
    temporary = state.get("temporaryMeds", [])
    discontinued = state.get("discontinuedMeds", [])

    # Penicillin allergy should be removed
    penicillin = any(a.get("allergen") == "Penicillin" for a in allergies)
    if penicillin:
        return False, "Penicillin allergy still present — should be removed (cleared by testing)"

    # Amoxicillin 500mg should be discontinued
    amox_active = any(
        m.get("medicationName") == "Amoxicillin 500mg capsule" for m in temporary
    )
    if amox_active:
        return False, "Amoxicillin 500mg capsule still in temporaryMeds — should be discontinued"

    amox_disc = any(
        m.get("medicationName") == "Amoxicillin 500mg capsule" for m in discontinued
    )
    if not amox_disc:
        return False, "Amoxicillin 500mg capsule not found in discontinuedMeds"

    # Amoxicillin-Clavulanate should be prescribed as temporary
    amox_clav = None
    for med in temporary:
        name = med.get("medicationName", "").lower()
        if "amoxicillin" in name and "clavulanate" in name:
            amox_clav = med
            break

    if amox_clav is None:
        return False, "Amoxicillin-Clavulanate not found in temporaryMeds"

    if amox_clav.get("pharmacyId") != "pharm_001":
        return False, f"Amoxicillin-Clavulanate pharmacy is '{amox_clav.get('pharmacyName')}', expected CVS #4521"
    if amox_clav.get("qty") != 20:
        return False, f"Amoxicillin-Clavulanate qty is {amox_clav.get('qty')}, expected 20"
    if amox_clav.get("refills") != 0:
        return False, f"Amoxicillin-Clavulanate refills is {amox_clav.get('refills')}, expected 0"
    if amox_clav.get("daysSupply") != 10:
        return False, f"Amoxicillin-Clavulanate daysSupply is {amox_clav.get('daysSupply')}, expected 10"

    return True, "Penicillin allergy removed; Amoxicillin discontinued; Amoxicillin-Clavulanate prescribed"
