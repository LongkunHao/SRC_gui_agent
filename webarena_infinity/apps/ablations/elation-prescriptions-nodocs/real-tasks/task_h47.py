import requests


def verify(server_url: str) -> tuple[bool, str]:
    """Cross-patient antibiotics: Cipro for Aisha, Cephalexin for David."""
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."

    state = resp.json()
    errors = []
    seed_ids = {f"rx_{str(i).zfill(3)}" for i in range(1, 31)}

    # Ciprofloxacin for Aisha Rahman (pat_003)
    cipro = [
        rx for rx in state["prescriptions"]
        if rx["id"] not in seed_ids
        and rx.get("patientId") == "pat_003"
        and "ciprofloxacin" in rx.get("drugName", "").lower()
    ]
    if not cipro:
        errors.append("No new Ciprofloxacin prescription found for Aisha Rahman (pat_003).")
    else:
        rx = cipro[0]
        if "500mg" not in rx.get("formStrength", "").replace(" ", ""):
            errors.append(f"Expected Cipro formStrength containing '500mg', got '{rx.get('formStrength')}'.")
        if rx.get("frequency") != "Twice daily":
            errors.append(f"Expected Cipro frequency 'Twice daily', got '{rx.get('frequency')}'.")
        if rx.get("quantity") != 14:
            errors.append(f"Expected Cipro quantity 14, got {rx.get('quantity')}.")
        if rx.get("refillsTotal") != 0:
            errors.append(f"Expected Cipro refillsTotal 0, got {rx.get('refillsTotal')}.")
        if rx.get("pharmacyId") != "pharm_002":
            errors.append(f"Expected Cipro pharmacyId 'pharm_002' (Walgreens), got '{rx.get('pharmacyId')}'.")

    # Cephalexin for David Kowalski (pat_002)
    keflex = [
        rx for rx in state["prescriptions"]
        if rx["id"] not in seed_ids
        and rx.get("patientId") == "pat_002"
        and "cephalexin" in rx.get("drugName", "").lower()
    ]
    if not keflex:
        errors.append("No new Cephalexin prescription found for David Kowalski (pat_002).")
    else:
        rx = keflex[0]
        if "500mg" not in rx.get("formStrength", "").replace(" ", ""):
            errors.append(f"Expected Keflex formStrength containing '500mg', got '{rx.get('formStrength')}'.")
        if rx.get("frequency") != "Four times daily":
            errors.append(f"Expected Keflex frequency 'Four times daily', got '{rx.get('frequency')}'.")
        if rx.get("quantity") != 28:
            errors.append(f"Expected Keflex quantity 28, got {rx.get('quantity')}.")
        if rx.get("refillsTotal") != 0:
            errors.append(f"Expected Keflex refillsTotal 0, got {rx.get('refillsTotal')}.")
        if rx.get("pharmacyId") != "pharm_003":
            errors.append(f"Expected Keflex pharmacyId 'pharm_003' (Rite Aid), got '{rx.get('pharmacyId')}'.")

    if errors:
        return False, " ".join(errors)
    return True, "Both antibiotics prescribed correctly: Cipro for Aisha, Cephalexin for David."
