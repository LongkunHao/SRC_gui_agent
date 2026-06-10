import requests


def verify(server_url: str) -> tuple[bool, str]:
    try:
        resp = requests.get(f"{server_url}/api/state")
        if resp.status_code != 200:
            return False, f"Failed to fetch state: HTTP {resp.status_code}"
        state = resp.json()
    except Exception as e:
        return False, f"Error fetching state: {e}"

    permanent_rx = state.get("permanentRxMeds", [])

    # Find Duloxetine 60mg
    duloxetine = None
    for med in permanent_rx:
        name = med.get("medicationName", "").lower()
        if "duloxetine" in name and "60mg" in name:
            duloxetine = med
            break

    if duloxetine is None:
        return False, "Duloxetine 60mg not found in permanentRxMeds"

    # Check dispense as written
    if not duloxetine.get("dispenseAsWritten"):
        return False, "Duloxetine should be marked as dispense as written"

    # Check two diagnoses
    diagnoses = duloxetine.get("diagnosis", [])
    diag_codes = {d.get("code") for d in diagnoses}
    if "M54.5" not in diag_codes:
        return False, f"Missing chronic low back pain diagnosis (M54.5), got: {diag_codes}"
    if "F41.1" not in diag_codes:
        return False, f"Missing generalized anxiety disorder diagnosis (F41.1), got: {diag_codes}"

    # Check prescription details
    if duloxetine.get("pharmacyId") != "pharm_001":
        return False, f"Duloxetine pharmacy is '{duloxetine.get('pharmacyName')}', expected CVS #4521"
    if duloxetine.get("qty") != 30:
        return False, f"Duloxetine qty is {duloxetine.get('qty')}, expected 30"
    if duloxetine.get("refills") != 5:
        return False, f"Duloxetine refills is {duloxetine.get('refills')}, expected 5"
    if duloxetine.get("daysSupply") != 30:
        return False, f"Duloxetine daysSupply is {duloxetine.get('daysSupply')}, expected 30"

    return True, "Duloxetine 60mg prescribed with DAW and dual diagnoses (M54.5 + F41.1)"
