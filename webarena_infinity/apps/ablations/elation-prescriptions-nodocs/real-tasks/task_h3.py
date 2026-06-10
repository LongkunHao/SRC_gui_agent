import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."

    state = resp.json()

    # Check current patient is William Thornton
    if state.get("currentPatientId") != "pat_004":
        return False, f"Expected currentPatientId 'pat_004' (William Thornton), got '{state.get('currentPatientId')}'."

    errors = []

    # Check rr_010 (Furosemide refill) is approved
    refill_requests = state.get("refillRequests", [])
    rr_010 = None
    for rr in refill_requests:
        if rr.get("id") == "rr_010":
            rr_010 = rr
            break

    if rr_010 is None:
        errors.append("Refill request rr_010 (Furosemide) not found.")
    elif rr_010.get("status") != "approved":
        errors.append(f"Expected rr_010 (Furosemide) status 'approved', got '{rr_010.get('status')}'.")

    # Check rr_007 (Valsartan refill) is denied
    rr_007 = None
    for rr in refill_requests:
        if rr.get("id") == "rr_007":
            rr_007 = rr
            break

    if rr_007 is None:
        errors.append("Refill request rr_007 (Valsartan) not found.")
    elif rr_007.get("status") != "denied":
        errors.append(f"Expected rr_007 (Valsartan) status 'denied', got '{rr_007.get('status')}'.")

    # Check rx_023 (Insulin Glargine) dosage contains "30"
    prescriptions = state.get("prescriptions", [])
    rx_023 = None
    for rx in prescriptions:
        if rx.get("id") == "rx_023":
            rx_023 = rx
            break

    if rx_023 is None:
        errors.append("Prescription rx_023 (Insulin Glargine) not found.")
    elif "30" not in str(rx_023.get("dosage", "")):
        errors.append(f"Expected rx_023 dosage to contain '30', got '{rx_023.get('dosage')}'.")

    if errors:
        return False, " ".join(errors)

    return True, "Furosemide refill approved, Valsartan refill denied, and Insulin dose increased to 30 units."
