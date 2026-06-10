import requests


def verify(server_url: str) -> tuple[bool, str]:
    try:
        resp = requests.get(f"{server_url}/api/state")
        if resp.status_code != 200:
            return False, f"Failed to fetch state: HTTP {resp.status_code}"
        state = resp.json()
    except Exception as e:
        return False, f"Error fetching state: {e}"

    settings = state.get("settings", {})
    dds = settings.get("drugDecisionSupport", {})
    temporary = state.get("temporaryMeds", [])

    # Drug interaction alerts should be set to "all"
    if dds.get("drugToDrugLevel") != "all":
        return False, f"Drug interaction alert level is '{dds.get('drugToDrugLevel')}', expected 'all'"

    # Drug-to-allergy alerts should be enabled
    if not dds.get("drugToAllergyEnabled"):
        return False, "Drug-to-allergy alerts should be enabled"

    # Cephalexin 500mg should be prescribed as temporary
    cephalexin = None
    for med in temporary:
        name = med.get("medicationName", "").lower()
        if "cephalexin" in name and "500mg" in name:
            cephalexin = med
            break

    if cephalexin is None:
        return False, "Cephalexin 500mg not found in temporaryMeds"

    if cephalexin.get("pharmacyId") != "pharm_001":
        return False, f"Cephalexin pharmacy is '{cephalexin.get('pharmacyName')}', expected CVS #4521"
    if cephalexin.get("qty") != 30:
        return False, f"Cephalexin qty is {cephalexin.get('qty')}, expected 30"
    if cephalexin.get("refills") != 0:
        return False, f"Cephalexin refills is {cephalexin.get('refills')}, expected 0"
    if cephalexin.get("daysSupply") != 10:
        return False, f"Cephalexin daysSupply is {cephalexin.get('daysSupply')}, expected 10"

    return True, "Drug alerts set to All; Cephalexin 500mg prescribed as temporary at CVS"
