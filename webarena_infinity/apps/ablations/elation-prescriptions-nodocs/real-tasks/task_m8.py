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
        and "fluconazole" in rx.get("drugName", "").lower()
    ]

    if not matches:
        return False, "No new Fluconazole prescription found for Margaret Chen (pat_001)."

    rx = matches[0]

    if "150mg" not in rx.get("formStrength", "").lower():
        return False, f"Expected formStrength to contain '150mg', got '{rx.get('formStrength')}'."

    if rx.get("quantity") != 1:
        return False, f"Expected quantity 1, got {rx.get('quantity')}."

    if rx.get("refillsTotal") != 0:
        return False, f"Expected refillsTotal 0, got {rx.get('refillsTotal')}."

    if rx.get("pharmacyId") != "pharm_001":
        return False, f"Expected pharmacyId 'pharm_001' (CVS), got '{rx.get('pharmacyId')}'."

    return True, "Fluconazole 150mg prescribed correctly for Margaret Chen — one-time dose, qty 1, no refills, sent to CVS."
