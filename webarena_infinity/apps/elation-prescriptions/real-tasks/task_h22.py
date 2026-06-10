import requests


def verify(server_url: str) -> tuple[bool, str]:
    try:
        resp = requests.get(f"{server_url}/api/state")
        if resp.status_code != 200:
            return False, f"Failed to fetch state: HTTP {resp.status_code}"
        state = resp.json()
    except Exception as e:
        return False, f"Error fetching state: {e}"

    # Check Omeprazole refill is denied
    refill_requests = state.get("refillRequests", [])
    omeprazole_refill = None
    for req in refill_requests:
        if req.get("medicationName") == "Omeprazole 20mg capsule" or req.get("id") == "rr_004":
            omeprazole_refill = req
            break
    if omeprazole_refill is None:
        return False, "Omeprazole refill request not found"
    if omeprazole_refill.get("status") != "denied":
        return False, f"Omeprazole refill status is '{omeprazole_refill.get('status')}', expected 'denied'"

    # Check Omeprazole is discontinued
    permanent_rx = state.get("permanentRxMeds", [])
    discontinued = state.get("discontinuedMeds", [])
    for med in permanent_rx:
        if med.get("medicationName") == "Omeprazole 20mg capsule":
            return False, "Omeprazole 20mg capsule still in permanentRxMeds"

    omeprazole_disc = None
    for med in discontinued:
        if med.get("medicationName") == "Omeprazole 20mg capsule":
            omeprazole_disc = med
            break
    if omeprazole_disc is None:
        return False, "Omeprazole 20mg capsule not found in discontinuedMeds"

    # Check Pantoprazole 40mg prescribed
    pantoprazole = None
    for med in permanent_rx:
        name = med.get("medicationName", "").lower()
        if "pantoprazole" in name and "40mg" in name:
            pantoprazole = med
            break
    if pantoprazole is None:
        return False, "No Pantoprazole 40mg found in permanentRxMeds"

    qty = pantoprazole.get("qty")
    if qty != 30:
        return False, f"Pantoprazole qty is {qty}, expected 30"

    refills = pantoprazole.get("refills", pantoprazole.get("refillsRemaining"))
    if refills != 3:
        return False, f"Pantoprazole refills is {refills}, expected 3"

    pharmacy_id = pantoprazole.get("pharmacyId", "")
    pharmacy_name = pantoprazole.get("pharmacyName", "")
    if pharmacy_id != "pharm_001" and "cvs" not in pharmacy_name.lower():
        return False, f"Pantoprazole pharmacy is '{pharmacy_name}' ({pharmacy_id}), expected CVS #4521"

    return True, "Omeprazole refill denied, medication discontinued, Pantoprazole 40mg prescribed at CVS"
