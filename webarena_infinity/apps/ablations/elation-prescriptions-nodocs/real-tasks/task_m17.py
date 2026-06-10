import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."

    state = resp.json()

    if state.get("currentPatientId") != "pat_002":
        return False, f"Expected currentPatientId 'pat_002' (David Kowalski), got '{state.get('currentPatientId')}'."

    seed_ids = {f"rx_{str(i).zfill(3)}" for i in range(1, 31)}
    matches = [
        rx for rx in state["prescriptions"]
        if rx["id"] not in seed_ids
        and rx.get("patientId") == "pat_002"
        and "valacyclovir" in rx.get("drugName", "").lower()
    ]

    if not matches:
        return False, "No new Valacyclovir prescription found for David Kowalski (pat_002)."

    rx = matches[0]

    if "500mg" not in rx.get("formStrength", "").lower():
        return False, f"Expected formStrength to contain '500mg', got '{rx.get('formStrength')}'."

    if rx.get("frequency") != "Twice daily":
        return False, f"Expected frequency 'Twice daily', got '{rx.get('frequency')}'."

    if rx.get("quantity") != 20:
        return False, f"Expected quantity 20, got {rx.get('quantity')}."

    if rx.get("refillsTotal") != 0:
        return False, f"Expected refillsTotal 0, got {rx.get('refillsTotal')}."

    if rx.get("pharmacyId") != "pharm_003":
        return False, f"Expected pharmacyId 'pharm_003' (Rite Aid), got '{rx.get('pharmacyId')}'."

    return True, "Valacyclovir 500mg prescribed correctly for David Kowalski — twice daily, qty 20, no refills, sent to Rite Aid."
