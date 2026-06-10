import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."

    state = resp.json()

    if state.get("currentPatientId") != "pat_003":
        return False, f"Expected current patient pat_003 (Aisha Rahman), got '{state.get('currentPatientId')}'."

    prescriptions = state.get("prescriptions", [])
    seed_ids = {f"rx_{str(i).zfill(3)}" for i in range(1, 31)}

    matches = [
        rx for rx in prescriptions
        if rx.get("patientId") == "pat_003"
        and "ciprofloxacin" in rx.get("drugName", "").lower()
        and rx.get("id") not in seed_ids
    ]

    if not matches:
        return False, "No new Ciprofloxacin prescription found for pat_003."

    rx = matches[0]
    errors = []

    if "500mg" not in rx.get("formStrength", ""):
        errors.append(f"formStrength should contain '500mg', got '{rx.get('formStrength')}'")
    if rx.get("frequency") != "Twice daily":
        errors.append(f"frequency should be 'Twice daily', got '{rx.get('frequency')}'")
    if rx.get("route") != "Oral":
        errors.append(f"route should be 'Oral', got '{rx.get('route')}'")
    if rx.get("quantity") != 14:
        errors.append(f"quantity should be 14, got {rx.get('quantity')}")
    if rx.get("daysSupply") != 7:
        errors.append(f"daysSupply should be 7, got {rx.get('daysSupply')}")
    if rx.get("refillsTotal") != 0:
        errors.append(f"refillsTotal should be 0, got {rx.get('refillsTotal')}")
    if rx.get("pharmacyId") != "pharm_002":
        errors.append(f"pharmacyId should be 'pharm_002' (Walgreens), got '{rx.get('pharmacyId')}'")
    if rx.get("status") != "active":
        errors.append(f"status should be 'active', got '{rx.get('status')}'")

    if errors:
        return False, "New Ciprofloxacin prescription found but has issues: " + "; ".join(errors)

    return True, "Patient switched to Aisha Rahman and new Ciprofloxacin prescription is correct."
