import requests


def verify(server_url: str) -> tuple[bool, str]:
    """Specialty prescribing setup + Trulicity for Robert Fitzgerald."""
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."

    state = resp.json()
    errors = []
    settings = state.get("settings", {})

    # Settings checks
    if settings.get("defaultPharmacy") != "pharm_011":
        errors.append(f"Expected defaultPharmacy 'pharm_011' (Accredo), got '{settings.get('defaultPharmacy')}'.")
    if settings.get("defaultDaysSupply") != 28:
        errors.append(f"Expected defaultDaysSupply 28, got {settings.get('defaultDaysSupply')}.")
    if settings.get("defaultRefills") != 2:
        errors.append(f"Expected defaultRefills 2, got {settings.get('defaultRefills')}.")

    # New Trulicity/Dulaglutide prescription for Robert (pat_006)
    seed_ids = {f"rx_{str(i).zfill(3)}" for i in range(1, 31)}
    trulicity = [
        rx for rx in state["prescriptions"]
        if rx["id"] not in seed_ids
        and rx.get("patientId") == "pat_006"
        and ("dulaglutide" in rx.get("drugName", "").lower() or "trulicity" in rx.get("brandName", "").lower())
    ]

    if not trulicity:
        errors.append("No new Trulicity/Dulaglutide prescription found for Robert Fitzgerald (pat_006).")
    else:
        rx = trulicity[0]
        if "1.5mg" not in rx.get("formStrength", "").replace(" ", ""):
            errors.append(f"Expected formStrength containing '1.5mg', got '{rx.get('formStrength')}'.")
        if rx.get("frequency") != "Once weekly":
            errors.append(f"Expected frequency 'Once weekly', got '{rx.get('frequency')}'.")
        if rx.get("route") != "Subcutaneous":
            errors.append(f"Expected route 'Subcutaneous', got '{rx.get('route')}'.")
        if rx.get("quantity") != 1:
            errors.append(f"Expected quantity 1, got {rx.get('quantity')}.")
        if rx.get("daysSupply") != 28:
            errors.append(f"Expected daysSupply 28, got {rx.get('daysSupply')}.")
        if rx.get("refillsTotal", 0) < 2:
            errors.append(f"Expected refillsTotal >= 2, got {rx.get('refillsTotal')}.")
        if not rx.get("priorAuth"):
            errors.append("Expected priorAuth to be true.")
        if rx.get("priorAuthNumber") != "PA-2026-77777":
            errors.append(f"Expected priorAuthNumber 'PA-2026-77777', got '{rx.get('priorAuthNumber')}'.")
        if rx.get("pharmacyId") != "pharm_011":
            errors.append(f"Expected pharmacyId 'pharm_011' (Accredo), got '{rx.get('pharmacyId')}'.")

    if errors:
        return False, " ".join(errors)
    return True, "Specialty prescribing setup complete and Trulicity prescribed for Robert."
