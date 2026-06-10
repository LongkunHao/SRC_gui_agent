import requests


def verify(server_url: str) -> tuple[bool, str]:
    """No-allergy patient discovery: Nexium for Aisha Rahman."""
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."

    state = resp.json()
    errors = []
    seed_ids = {f"rx_{str(i).zfill(3)}" for i in range(1, 31)}

    # New Nexium/Esomeprazole for Aisha Rahman (pat_003 — no allergies)
    nexium = [
        rx for rx in state["prescriptions"]
        if rx["id"] not in seed_ids
        and rx.get("patientId") == "pat_003"
        and "esomeprazole" in rx.get("drugName", "").lower()
    ]
    if not nexium:
        errors.append("No new Esomeprazole/Nexium prescription found for Aisha Rahman (pat_003).")
    else:
        rx = nexium[0]
        if "40mg" not in rx.get("formStrength", "").replace(" ", ""):
            errors.append(f"Expected formStrength containing '40mg', got '{rx.get('formStrength')}'.")
        if rx.get("frequency") != "Once daily":
            errors.append(f"Expected frequency 'Once daily', got '{rx.get('frequency')}'.")
        if rx.get("quantity") != 30:
            errors.append(f"Expected quantity 30, got {rx.get('quantity')}.")
        if rx.get("refillsTotal") != 3:
            errors.append(f"Expected refillsTotal 3, got {rx.get('refillsTotal')}.")
        if rx.get("pharmacyId") != "pharm_002":
            errors.append(f"Expected pharmacyId 'pharm_002' (Walgreens), got '{rx.get('pharmacyId')}'.")

    if errors:
        return False, " ".join(errors)
    return True, "Nexium prescribed correctly for the no-allergy patient (Aisha Rahman)."
