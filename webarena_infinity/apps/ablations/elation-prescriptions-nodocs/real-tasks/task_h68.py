import requests


def verify(server_url: str) -> tuple[bool, str]:
    """Settings + prescribe Omeprazole for David and Aisha."""
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."

    state = resp.json()
    errors = []
    seed_ids = {f"rx_{str(i).zfill(3)}" for i in range(1, 31)}

    # Settings
    settings = state.get("settings", {})
    if settings.get("defaultPharmacy") != "pharm_002":
        errors.append(f"Expected defaultPharmacy 'pharm_002' (Walgreens), got '{settings.get('defaultPharmacy')}'.")
    if settings.get("printFormat") != "detailed":
        errors.append(f"Expected printFormat 'detailed', got '{settings.get('printFormat')}'.")

    # New Omeprazole for David (pat_002)
    david_ome = [
        rx for rx in state["prescriptions"]
        if rx["id"] not in seed_ids
        and rx.get("patientId") == "pat_002"
        and "omeprazole" in rx.get("drugName", "").lower()
    ]
    if not david_ome:
        errors.append("No new Omeprazole prescription found for David Kowalski.")
    else:
        rx = david_ome[0]
        if rx.get("pharmacyId") != "pharm_003":
            errors.append(f"Expected David's Omeprazole at Rite Aid (pharm_003), got '{rx.get('pharmacyId')}'.")
        if rx.get("quantity") != 30:
            errors.append(f"Expected David's Omeprazole quantity 30, got {rx.get('quantity')}.")
        if rx.get("refillsTotal", 0) < 2:
            errors.append(f"Expected David's Omeprazole refillsTotal >= 2, got {rx.get('refillsTotal')}.")

    # New Omeprazole for Aisha (pat_003)
    aisha_ome = [
        rx for rx in state["prescriptions"]
        if rx["id"] not in seed_ids
        and rx.get("patientId") == "pat_003"
        and "omeprazole" in rx.get("drugName", "").lower()
    ]
    if not aisha_ome:
        errors.append("No new Omeprazole prescription found for Aisha Rahman.")
    else:
        rx = aisha_ome[0]
        if rx.get("pharmacyId") != "pharm_002":
            errors.append(f"Expected Aisha's Omeprazole at Walgreens (pharm_002), got '{rx.get('pharmacyId')}'.")
        if rx.get("quantity") != 30:
            errors.append(f"Expected Aisha's Omeprazole quantity 30, got {rx.get('quantity')}.")
        if rx.get("refillsTotal", 0) < 2:
            errors.append(f"Expected Aisha's Omeprazole refillsTotal >= 2, got {rx.get('refillsTotal')}.")

    if errors:
        return False, " ".join(errors)
    return True, "Settings updated, Omeprazole prescribed for both David and Aisha."
