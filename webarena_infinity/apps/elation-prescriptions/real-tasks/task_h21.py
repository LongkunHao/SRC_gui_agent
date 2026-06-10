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
    discontinued = state.get("discontinuedMeds", [])
    canceled = state.get("canceledScripts", [])

    # Check Alprazolam is NOT in permanentRxMeds
    for med in permanent_rx:
        if "alprazolam" in med.get("medicationName", "").lower():
            return False, "Alprazolam still found in permanentRxMeds, expected it to be discontinued"

    # Check Alprazolam IS in discontinuedMeds
    alprazolam_disc = None
    for med in discontinued:
        if "alprazolam" in med.get("medicationName", "").lower():
            alprazolam_disc = med
            break
    if alprazolam_disc is None:
        return False, "Alprazolam not found in discontinuedMeds"

    # Check cancellation was sent
    alprazolam_cancel = None
    for script in canceled:
        if "alprazolam" in script.get("medicationName", "").lower():
            alprazolam_cancel = script
            break
    if alprazolam_cancel is None:
        return False, "No cancellation found for Alprazolam in canceledScripts"

    # Check Hydroxyzine 25mg prescribed
    hydroxyzine = None
    for med in permanent_rx:
        name = med.get("medicationName", "").lower()
        if "hydroxyzine" in name and "25mg" in name:
            hydroxyzine = med
            break
    if hydroxyzine is None:
        return False, "No Hydroxyzine 25mg found in permanentRxMeds"

    qty = hydroxyzine.get("qty")
    if qty != 60:
        return False, f"Hydroxyzine qty is {qty}, expected 60"

    refills = hydroxyzine.get("refills", hydroxyzine.get("refillsRemaining"))
    if refills != 3:
        return False, f"Hydroxyzine refills is {refills}, expected 3"

    pharmacy_id = hydroxyzine.get("pharmacyId", "")
    pharmacy_name = hydroxyzine.get("pharmacyName", "")
    if pharmacy_id != "pharm_001" and "cvs" not in pharmacy_name.lower():
        return False, f"Hydroxyzine pharmacy is '{pharmacy_name}' ({pharmacy_id}), expected CVS Pharmacy #4521"

    return True, "Alprazolam discontinued with cancellation, Hydroxyzine 25mg prescribed at CVS"
