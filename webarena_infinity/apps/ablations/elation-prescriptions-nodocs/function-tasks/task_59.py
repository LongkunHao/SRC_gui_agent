import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."

    state = resp.json()

    if state.get("currentPatientId") != "pat_006":
        return False, f"Expected current patient pat_006 (Robert Fitzgerald), got '{state.get('currentPatientId')}'."

    prescriptions = state.get("prescriptions", [])
    seed_ids = {f"rx_{str(i).zfill(3)}" for i in range(1, 31)}

    matches = [
        rx for rx in prescriptions
        if rx.get("patientId") == "pat_006"
        and "clopidogrel" in rx.get("drugName", "").lower()
        and rx.get("id") not in seed_ids
    ]

    if not matches:
        return False, "No new Clopidogrel prescription found for pat_006."

    rx = matches[0]
    errors = []

    if "75mg" not in rx.get("formStrength", ""):
        errors.append(f"formStrength should contain '75mg', got '{rx.get('formStrength')}'")
    if rx.get("frequency") != "Once daily":
        errors.append(f"frequency should be 'Once daily', got '{rx.get('frequency')}'")
    if rx.get("route") != "Oral":
        errors.append(f"route should be 'Oral', got '{rx.get('route')}'")
    if rx.get("quantity") != 30:
        errors.append(f"quantity should be 30, got {rx.get('quantity')}")
    if rx.get("daysSupply") != 30:
        errors.append(f"daysSupply should be 30, got {rx.get('daysSupply')}")
    if rx.get("refillsTotal") != 5:
        errors.append(f"refillsTotal should be 5, got {rx.get('refillsTotal')}")
    if rx.get("pharmacyId") != "pharm_004":
        errors.append(f"pharmacyId should be 'pharm_004' (UCSF), got '{rx.get('pharmacyId')}'")
    if rx.get("status") != "active":
        errors.append(f"status should be 'active', got '{rx.get('status')}'")

    if errors:
        return False, "New Clopidogrel prescription found but has issues: " + "; ".join(errors)

    return True, "Patient switched to Robert Fitzgerald and new Clopidogrel prescription is correct."
