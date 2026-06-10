import requests


def verify(server_url: str) -> tuple[bool, str]:
    try:
        resp = requests.get(f"{server_url}/api/state")
        if resp.status_code != 200:
            return False, f"Failed to fetch state: HTTP {resp.status_code}"
        state = resp.json()
    except Exception as e:
        return False, f"Error fetching state: {e}"

    temporary = state.get("temporaryMeds", [])
    permanent_rx = state.get("permanentRxMeds", [])
    discontinued = state.get("discontinuedMeds", [])
    temp_names = [m.get("medicationName", "") for m in temporary]

    # Prednisone (corticosteroid) should be discontinued
    if "Prednisone 10mg tablet" in temp_names:
        return False, "Prednisone 10mg tablet still in temporaryMeds, should be discontinued"
    prednisone_disc = None
    for med in discontinued:
        if med.get("medicationName") == "Prednisone 10mg tablet":
            prednisone_disc = med
            break
    if prednisone_disc is None:
        return False, "Prednisone 10mg tablet not found in discontinuedMeds"

    # Amoxicillin (penicillin antibiotic) should be discontinued
    if "Amoxicillin 500mg capsule" in temp_names:
        return False, "Amoxicillin 500mg capsule still in temporaryMeds, should be discontinued"
    amoxicillin_disc = None
    for med in discontinued:
        if med.get("medicationName") == "Amoxicillin 500mg capsule":
            amoxicillin_disc = med
            break
    if amoxicillin_disc is None:
        return False, "Amoxicillin 500mg capsule not found in discontinuedMeds"

    # Ciprofloxacin should be moved to permanent Rx
    if "Ciprofloxacin 500mg tablet" in temp_names:
        return False, "Ciprofloxacin 500mg tablet still in temporaryMeds, should be moved to permanent"
    cipro_perm = None
    for med in permanent_rx:
        if med.get("medicationName") == "Ciprofloxacin 500mg tablet":
            cipro_perm = med
            break
    if cipro_perm is None:
        return False, "Ciprofloxacin 500mg tablet not found in permanentRxMeds"
    if cipro_perm.get("classification") != "permanent_rx":
        return False, f"Ciprofloxacin classification is '{cipro_perm.get('classification')}', expected 'permanent_rx'"

    return True, "Prednisone and Amoxicillin discontinued, Ciprofloxacin moved to permanent Rx"
