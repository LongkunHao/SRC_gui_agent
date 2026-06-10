import requests


def verify(server_url: str) -> tuple[bool, str]:
    """Back injury treatment: Diclofenac + Cyclobenzaprine for Margaret."""
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."

    state = resp.json()
    errors = []
    seed_ids = {f"rx_{str(i).zfill(3)}" for i in range(1, 31)}

    # Diclofenac for Margaret
    diclo = [
        rx for rx in state["prescriptions"]
        if rx["id"] not in seed_ids
        and rx.get("patientId") == "pat_001"
        and "diclofenac" in rx.get("drugName", "").lower()
    ]
    if not diclo:
        errors.append("No new Diclofenac prescription found for Margaret.")
    else:
        rx = diclo[0]
        if "50mg" not in rx.get("formStrength", "").replace(" ", ""):
            errors.append(f"Expected Diclofenac formStrength containing '50mg', got '{rx.get('formStrength')}'.")
        if rx.get("frequency") != "Twice daily":
            errors.append(f"Expected Diclofenac frequency 'Twice daily', got '{rx.get('frequency')}'.")
        if rx.get("quantity") != 60:
            errors.append(f"Expected Diclofenac quantity 60, got {rx.get('quantity')}.")
        if rx.get("refillsTotal") != 2:
            errors.append(f"Expected Diclofenac refillsTotal 2, got {rx.get('refillsTotal')}.")
        if rx.get("pharmacyId") != "pharm_001":
            errors.append(f"Expected Diclofenac pharmacyId 'pharm_001' (CVS), got '{rx.get('pharmacyId')}'.")

    # Cyclobenzaprine for Margaret
    flexeril = [
        rx for rx in state["prescriptions"]
        if rx["id"] not in seed_ids
        and rx.get("patientId") == "pat_001"
        and "cyclobenzaprine" in rx.get("drugName", "").lower()
    ]
    if not flexeril:
        errors.append("No new Cyclobenzaprine prescription found for Margaret.")
    else:
        rx = flexeril[0]
        if "5mg" not in rx.get("formStrength", "").replace(" ", ""):
            errors.append(f"Expected Cyclobenzaprine formStrength containing '5mg', got '{rx.get('formStrength')}'.")
        if rx.get("frequency") != "Three times daily":
            errors.append(f"Expected Cyclobenzaprine frequency 'Three times daily', got '{rx.get('frequency')}'.")
        if rx.get("quantity") != 90:
            errors.append(f"Expected Cyclobenzaprine quantity 90, got {rx.get('quantity')}.")
        if rx.get("refillsTotal") != 1:
            errors.append(f"Expected Cyclobenzaprine refillsTotal 1, got {rx.get('refillsTotal')}.")
        if rx.get("pharmacyId") != "pharm_001":
            errors.append(f"Expected Cyclobenzaprine pharmacyId 'pharm_001' (CVS), got '{rx.get('pharmacyId')}'.")

    if errors:
        return False, " ".join(errors)
    return True, "Both back injury medications prescribed correctly for Margaret."
