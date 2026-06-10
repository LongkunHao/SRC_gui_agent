import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."

    state = resp.json()

    if state.get("currentPatientId") != "pat_005":
        return False, f"Expected current patient pat_005 (Jessica Morales), got '{state.get('currentPatientId')}'."

    prescriptions = state.get("prescriptions", [])
    seed_ids = {f"rx_{str(i).zfill(3)}" for i in range(1, 31)}

    matches = [
        rx for rx in prescriptions
        if rx.get("patientId") == "pat_005"
        and "valacyclovir" in rx.get("drugName", "").lower()
        and rx.get("id") not in seed_ids
    ]

    if not matches:
        return False, "No new Valacyclovir prescription found for pat_005."

    rx = matches[0]
    errors = []

    if "500mg" not in rx.get("formStrength", ""):
        errors.append(f"formStrength should contain '500mg', got '{rx.get('formStrength')}'")
    if rx.get("frequency") != "Twice daily":
        errors.append(f"frequency should be 'Twice daily', got '{rx.get('frequency')}'")
    if rx.get("route") != "Oral":
        errors.append(f"route should be 'Oral', got '{rx.get('route')}'")
    if rx.get("quantity") != 20:
        errors.append(f"quantity should be 20, got {rx.get('quantity')}")
    if rx.get("daysSupply") != 10:
        errors.append(f"daysSupply should be 10, got {rx.get('daysSupply')}")
    if rx.get("refillsTotal") != 0:
        errors.append(f"refillsTotal should be 0, got {rx.get('refillsTotal')}")
    if rx.get("pharmacyId") != "pharm_001":
        errors.append(f"pharmacyId should be 'pharm_001' (CVS), got '{rx.get('pharmacyId')}'")
    if rx.get("status") != "active":
        errors.append(f"status should be 'active', got '{rx.get('status')}'")

    if errors:
        return False, "New Valacyclovir prescription found but has issues: " + "; ".join(errors)

    return True, "Patient switched to Jessica Morales and new Valacyclovir prescription is correct."
