import requests


def verify(server_url: str) -> tuple[bool, str]:
    try:
        resp = requests.get(f"{server_url}/api/state")
        if resp.status_code != 200:
            return False, f"Failed to fetch state: HTTP {resp.status_code}"
        state = resp.json()
    except Exception as e:
        return False, f"Error fetching state: {e}"

    otc_meds = state.get("permanentOtcMeds", [])
    discontinued = state.get("discontinuedMeds", [])
    patient = state.get("currentPatient", {})

    # Check Fish Oil is NOT in permanentOtcMeds
    for med in otc_meds:
        if "fish oil" in med.get("medicationName", "").lower():
            return False, "Fish Oil still found in permanentOtcMeds"

    # Check Fish Oil IS in discontinuedMeds
    fish_oil_disc = None
    for med in discontinued:
        if "fish oil" in med.get("medicationName", "").lower():
            fish_oil_disc = med
            break
    if fish_oil_disc is None:
        return False, "Fish Oil not found in discontinuedMeds"

    # Check lastReconciledDate was updated (should be newer than seed value)
    reconciled = patient.get("lastReconciledDate", "")
    if not reconciled or reconciled == "2026-01-15T14:30:00Z":
        return False, f"lastReconciledDate not updated (still '{reconciled}')"

    # Check Turmeric OTC documented
    turmeric = None
    for med in otc_meds:
        if "turmeric" in med.get("medicationName", "").lower():
            turmeric = med
            break
    if turmeric is None:
        return False, "Turmeric not found in permanentOtcMeds"

    if turmeric.get("classification") != "permanent_otc":
        return False, f"Turmeric classification is '{turmeric.get('classification')}', expected 'permanent_otc'"

    return True, "Med rec completed: Fish Oil discontinued, Turmeric documented as OTC"
