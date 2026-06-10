import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."

    state = resp.json()

    if state.get("currentPatientId") != "pat_004":
        return False, f"Expected current patient pat_004 (William Thornton), got '{state.get('currentPatientId')}'."

    prescriptions = state.get("prescriptions", [])
    seed_ids = {f"rx_{str(i).zfill(3)}" for i in range(1, 31)}

    matches = [
        rx for rx in prescriptions
        if rx.get("patientId") == "pat_004"
        and ("fluticasone" in rx.get("drugName", "").lower() or "salmeterol" in rx.get("drugName", "").lower())
        and rx.get("id") not in seed_ids
    ]

    if not matches:
        return False, "No new Fluticasone/Salmeterol (Advair) prescription found for pat_004."

    rx = matches[0]
    errors = []

    if "250/50" not in rx.get("formStrength", ""):
        errors.append(f"formStrength should contain '250/50', got '{rx.get('formStrength')}'")
    if rx.get("route") != "Inhalation":
        errors.append(f"route should be 'Inhalation', got '{rx.get('route')}'")
    if rx.get("frequency") != "Twice daily":
        errors.append(f"frequency should be 'Twice daily', got '{rx.get('frequency')}'")
    if rx.get("quantity") != 1:
        errors.append(f"quantity should be 1, got {rx.get('quantity')}")
    if rx.get("daysSupply") != 30:
        errors.append(f"daysSupply should be 30, got {rx.get('daysSupply')}")
    if rx.get("refillsTotal") != 2:
        errors.append(f"refillsTotal should be 2, got {rx.get('refillsTotal')}")
    if rx.get("pharmacyId") != "pharm_005":
        errors.append(f"pharmacyId should be 'pharm_005' (Kaiser), got '{rx.get('pharmacyId')}'")
    if rx.get("status") != "active":
        errors.append(f"status should be 'active', got '{rx.get('status')}'")

    if errors:
        return False, "New Advair prescription found but has issues: " + "; ".join(errors)

    return True, "Patient switched to William Thornton and new Advair Diskus inhalation prescription is correct."
