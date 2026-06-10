import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."

    state = resp.json()

    if state.get("currentPatientId") != "pat_002":
        return False, f"Expected current patient pat_002 (David Kowalski), got '{state.get('currentPatientId')}'."

    prescriptions = state.get("prescriptions", [])
    seed_ids = {f"rx_{str(i).zfill(3)}" for i in range(1, 31)}

    matches = [
        rx for rx in prescriptions
        if rx.get("patientId") == "pat_002"
        and "alprazolam" in rx.get("drugName", "").lower()
        and rx.get("id") not in seed_ids
    ]

    if not matches:
        return False, "No new Alprazolam prescription found for pat_002."

    rx = matches[0]
    errors = []

    if "0.25mg" not in rx.get("formStrength", ""):
        errors.append(f"formStrength should contain '0.25mg', got '{rx.get('formStrength')}'")
    if rx.get("route") != "Oral":
        errors.append(f"route should be 'Oral', got '{rx.get('route')}'")
    if rx.get("quantity") != 60:
        errors.append(f"quantity should be 60, got {rx.get('quantity')}")
    if rx.get("daysSupply") != 30:
        errors.append(f"daysSupply should be 30, got {rx.get('daysSupply')}")
    if rx.get("refillsTotal") != 0:
        errors.append(f"refillsTotal should be 0, got {rx.get('refillsTotal')}")
    if rx.get("pharmacyId") != "pharm_003":
        errors.append(f"pharmacyId should be 'pharm_003' (Rite Aid), got '{rx.get('pharmacyId')}'")
    if rx.get("status") != "active":
        errors.append(f"status should be 'active', got '{rx.get('status')}'")

    if errors:
        return False, "New Alprazolam prescription found but has issues: " + "; ".join(errors)

    return True, "Patient switched to David Kowalski and new Alprazolam (Schedule IV) prescription is correct."
