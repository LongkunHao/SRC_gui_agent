import requests


def verify(server_url: str) -> tuple[bool, str]:
    """Settings changes + Cyclobenzaprine for David Kowalski."""
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."

    state = resp.json()
    errors = []
    settings = state.get("settings", {})

    # Settings
    if settings.get("signatureRequired") is not False:
        errors.append(f"Expected signatureRequired False, got {settings.get('signatureRequired')}.")
    if settings.get("printFormat") != "compact":
        errors.append(f"Expected printFormat 'compact', got '{settings.get('printFormat')}'.")

    # New Cyclobenzaprine for David (pat_002)
    seed_ids = {f"rx_{str(i).zfill(3)}" for i in range(1, 31)}
    flexeril = [
        rx for rx in state["prescriptions"]
        if rx["id"] not in seed_ids
        and rx.get("patientId") == "pat_002"
        and "cyclobenzaprine" in rx.get("drugName", "").lower()
    ]
    if not flexeril:
        errors.append("No new Cyclobenzaprine prescription found for David Kowalski (pat_002).")
    else:
        rx = flexeril[0]
        if "10mg" not in rx.get("formStrength", "").replace(" ", ""):
            errors.append(f"Expected formStrength containing '10mg', got '{rx.get('formStrength')}'.")
        if rx.get("frequency") != "Three times daily":
            errors.append(f"Expected frequency 'Three times daily', got '{rx.get('frequency')}'.")
        if rx.get("quantity") != 90:
            errors.append(f"Expected quantity 90, got {rx.get('quantity')}.")
        if rx.get("refillsTotal") != 1:
            errors.append(f"Expected refillsTotal 1, got {rx.get('refillsTotal')}.")
        if rx.get("pharmacyId") != "pharm_003":
            errors.append(f"Expected pharmacyId 'pharm_003' (Rite Aid), got '{rx.get('pharmacyId')}'.")

    if errors:
        return False, " ".join(errors)
    return True, "Settings updated and Cyclobenzaprine prescribed for David."
