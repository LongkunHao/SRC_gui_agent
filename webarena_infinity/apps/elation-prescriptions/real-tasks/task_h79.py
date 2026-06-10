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
    refill_requests = state.get("refillRequests", [])
    permanent_rx = state.get("permanentRxMeds", [])

    # Naproxen allergy should exist
    naproxen_allergy = None
    for a in allergies:
        if a.get("allergen", "").lower() == "naproxen":
            naproxen_allergy = a
            break

    if naproxen_allergy is None:
        return False, "Naproxen allergy not found in patient allergies"
    if naproxen_allergy.get("severity") != "Moderate":
        return False, f"Naproxen allergy severity is '{naproxen_allergy.get('severity')}', expected 'Moderate'"
    if naproxen_allergy.get("type") != "drug":
        return False, f"Naproxen allergy type is '{naproxen_allergy.get('type')}', expected 'drug'"

    # Omeprazole refill should be denied
    omep_rr = None
    for r in refill_requests:
        if r.get("medicationName") == "Omeprazole 20mg capsule":
            omep_rr = r
            break
    if omep_rr is None:
        return False, "Omeprazole refill request not found"
    if omep_rr.get("status") != "denied":
        return False, f"Omeprazole refill status is '{omep_rr.get('status')}', expected 'denied'"

    # Famotidine 20mg should be prescribed
    famotidine = None
    for med in permanent_rx:
        name = med.get("medicationName", "").lower()
        if "famotidine" in name and "20mg" in name:
            famotidine = med
            break

    if famotidine is None:
        return False, "Famotidine 20mg not found in permanentRxMeds"

    if famotidine.get("pharmacyId") != "pharm_001":
        return False, f"Famotidine pharmacy is '{famotidine.get('pharmacyName')}', expected CVS #4521"
    if famotidine.get("qty") != 30:
        return False, f"Famotidine qty is {famotidine.get('qty')}, expected 30"
    if famotidine.get("refills") != 3:
        return False, f"Famotidine refills is {famotidine.get('refills')}, expected 3"
    if famotidine.get("daysSupply") != 30:
        return False, f"Famotidine daysSupply is {famotidine.get('daysSupply')}, expected 30"

    return True, "Naproxen allergy added; Omeprazole refill denied; Famotidine 20mg prescribed"
