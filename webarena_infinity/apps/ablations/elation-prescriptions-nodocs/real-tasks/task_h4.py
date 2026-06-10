import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."

    state = resp.json()

    # Check current patient is Aisha Rahman
    if state.get("currentPatientId") != "pat_003":
        return False, f"Expected currentPatientId 'pat_003' (Aisha Rahman), got '{state.get('currentPatientId')}'."

    prescriptions = state.get("prescriptions", [])
    seed_ids = {f"rx_{str(i).zfill(3)}" for i in range(1, 31)}
    errors = []

    # Find new Amoxicillin prescription for pat_003
    amox_matches = [
        rx for rx in prescriptions
        if rx["id"] not in seed_ids
        and rx.get("patientId") == "pat_003"
        and "amoxicillin" in rx.get("drugName", "").lower()
    ]

    if not amox_matches:
        errors.append("No new Amoxicillin prescription found for Aisha Rahman (pat_003).")
    else:
        amox = amox_matches[0]
        if "500mg" not in amox.get("formStrength", "").lower().replace(" ", ""):
            errors.append(f"Amoxicillin: expected formStrength to contain '500mg', got '{amox.get('formStrength')}'.")
        if amox.get("quantity") != 30:
            errors.append(f"Amoxicillin: expected quantity 30, got {amox.get('quantity')}.")
        if amox.get("refillsTotal") != 0:
            errors.append(f"Amoxicillin: expected refillsTotal 0, got {amox.get('refillsTotal')}.")
        if amox.get("pharmacyId") != "pharm_002":
            errors.append(f"Amoxicillin: expected pharmacyId 'pharm_002' (Walgreens), got '{amox.get('pharmacyId')}'.")

    # Find new Prednisone prescription for pat_003
    pred_matches = [
        rx for rx in prescriptions
        if rx["id"] not in seed_ids
        and rx.get("patientId") == "pat_003"
        and "prednisone" in rx.get("drugName", "").lower()
    ]

    if not pred_matches:
        errors.append("No new Prednisone prescription found for Aisha Rahman (pat_003).")
    else:
        pred = pred_matches[0]
        if "20mg" not in pred.get("formStrength", "").lower().replace(" ", ""):
            errors.append(f"Prednisone: expected formStrength to contain '20mg', got '{pred.get('formStrength')}'.")
        if pred.get("quantity") != 5:
            errors.append(f"Prednisone: expected quantity 5, got {pred.get('quantity')}.")
        if pred.get("refillsTotal") != 0:
            errors.append(f"Prednisone: expected refillsTotal 0, got {pred.get('refillsTotal')}.")
        if pred.get("pharmacyId") != "pharm_002":
            errors.append(f"Prednisone: expected pharmacyId 'pharm_002' (Walgreens), got '{pred.get('pharmacyId')}'.")

    if errors:
        return False, " ".join(errors)

    return True, "Both Amoxicillin and Prednisone prescribed correctly for Aisha Rahman, sent to Walgreens."
