import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."

    state = resp.json()

    seed_ids = {f"rx_{str(i).zfill(3)}" for i in range(1, 31)}
    matches = [
        rx for rx in state["prescriptions"]
        if rx["id"] not in seed_ids
        and rx.get("patientId") == "pat_001"
        and "ciprofloxacin" in rx.get("drugName", "").lower()
    ]

    if not matches:
        return False, "No new Ciprofloxacin prescription found for Margaret Chen (pat_001)."

    rx = matches[0]

    if "500mg" not in rx.get("formStrength", "").lower():
        return False, f"Expected formStrength to contain '500mg', got '{rx.get('formStrength')}'."

    if rx.get("frequency") != "Twice daily":
        return False, f"Expected frequency 'Twice daily', got '{rx.get('frequency')}'."

    if rx.get("quantity") != 14:
        return False, f"Expected quantity 14, got {rx.get('quantity')}."

    if rx.get("refillsTotal") != 0:
        return False, f"Expected refillsTotal 0, got {rx.get('refillsTotal')}."

    if rx.get("route") != "Oral":
        return False, f"Expected route 'Oral', got '{rx.get('route')}'."

    if rx.get("pharmacyId") != "pharm_001":
        return False, f"Expected pharmacyId 'pharm_001' (CVS), got '{rx.get('pharmacyId')}'."

    if rx.get("status") != "active":
        return False, f"Expected status 'active', got '{rx.get('status')}'."

    return True, "Ciprofloxacin 500mg prescribed correctly for Margaret Chen — twice daily, qty 14, no refills, sent to CVS."
