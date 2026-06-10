import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."

    state = resp.json()

    # Check current patient is Robert Fitzgerald
    if state.get("currentPatientId") != "pat_006":
        return False, f"Expected currentPatientId 'pat_006' (Robert Fitzgerald), got '{state.get('currentPatientId')}'."

    prescriptions = state.get("prescriptions", [])

    # Find new Semaglutide (Ozempic) prescription for pat_006
    seed_ids = {f"rx_{str(i).zfill(3)}" for i in range(1, 31)}
    matches = [
        rx for rx in prescriptions
        if rx["id"] not in seed_ids
        and rx.get("patientId") == "pat_006"
        and "semaglutide" in rx.get("drugName", "").lower()
    ]

    if not matches:
        return False, "No new Semaglutide (Ozempic) prescription found for Robert Fitzgerald (pat_006)."

    new_rx = matches[0]
    errors = []

    if "0.5mg" not in new_rx.get("formStrength", "").lower().replace(" ", ""):
        errors.append(f"Expected formStrength to contain '0.5mg', got '{new_rx.get('formStrength')}'.")

    if new_rx.get("route") != "Subcutaneous":
        errors.append(f"Expected route 'Subcutaneous', got '{new_rx.get('route')}'.")

    if new_rx.get("quantity") != 1:
        errors.append(f"Expected quantity 1, got {new_rx.get('quantity')}.")

    if new_rx.get("daysSupply") != 28:
        errors.append(f"Expected daysSupply 28, got {new_rx.get('daysSupply')}.")

    if new_rx.get("refillsTotal") != 2:
        errors.append(f"Expected refillsTotal 2, got {new_rx.get('refillsTotal')}.")

    if new_rx.get("priorAuth") is not True:
        errors.append(f"Expected priorAuth to be True, got {new_rx.get('priorAuth')}.")

    if new_rx.get("priorAuthNumber") != "PA-2026-55555":
        errors.append(f"Expected priorAuthNumber 'PA-2026-55555', got '{new_rx.get('priorAuthNumber')}'.")

    if new_rx.get("pharmacyId") != "pharm_010":
        errors.append(f"Expected pharmacyId 'pharm_010' (BioPlus Specialty), got '{new_rx.get('pharmacyId')}'.")

    if errors:
        return False, "New Semaglutide prescription found but has issues: " + " ".join(errors)

    return True, "Ozempic (Semaglutide) 0.5mg prescribed correctly for Robert Fitzgerald with prior authorization."
