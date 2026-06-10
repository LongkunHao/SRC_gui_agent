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
        and "fluticasone" in rx.get("drugName", "").lower()
        and rx.get("id") not in seed_ids
    ]

    if not matches:
        return False, "No new Fluticasone Nasal prescription found for pat_003."

    rx = matches[0]
    errors = []

    if "50mcg" not in rx.get("formStrength", ""):
        errors.append(f"formStrength should contain '50mcg', got '{rx.get('formStrength')}'")
    if rx.get("route") != "Intranasal":
        errors.append(f"route should be 'Intranasal', got '{rx.get('route')}'")
    if rx.get("frequency") != "Once daily":
        errors.append(f"frequency should be 'Once daily', got '{rx.get('frequency')}'")
    if rx.get("quantity") != 1:
        errors.append(f"quantity should be 1, got {rx.get('quantity')}")
    if rx.get("daysSupply") != 30:
        errors.append(f"daysSupply should be 30, got {rx.get('daysSupply')}")
    if rx.get("refillsTotal") != 3:
        errors.append(f"refillsTotal should be 3, got {rx.get('refillsTotal')}")
    if rx.get("pharmacyId") != "pharm_002":
        errors.append(f"pharmacyId should be 'pharm_002' (Walgreens), got '{rx.get('pharmacyId')}'")
    if rx.get("status") != "active":
        errors.append(f"status should be 'active', got '{rx.get('status')}'")

    if errors:
        return False, "New Fluticasone Nasal prescription found but has issues: " + "; ".join(errors)

    return True, "Patient switched to Aisha Rahman and new Flonase intranasal prescription is correct."
