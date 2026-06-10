import requests


def verify(server_url: str) -> tuple[bool, str]:
    """Prednisone for William (Kaiser) and Jessica (CVS)."""
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."

    state = resp.json()
    errors = []
    seed_ids = {f"rx_{str(i).zfill(3)}" for i in range(1, 31)}

    # New Prednisone for William (pat_004) → Kaiser (pharm_005)
    will_pred = [
        rx for rx in state["prescriptions"]
        if rx["id"] not in seed_ids
        and rx.get("patientId") == "pat_004"
        and "prednisone" in rx.get("drugName", "").lower()
    ]
    if not will_pred:
        errors.append("No new Prednisone prescription found for William Thornton.")
    else:
        rx = will_pred[0]
        if rx.get("pharmacyId") != "pharm_005":
            errors.append(f"Expected William's Prednisone at Kaiser (pharm_005), got '{rx.get('pharmacyId')}'.")
        if rx.get("quantity") != 5:
            errors.append(f"Expected quantity 5, got {rx.get('quantity')}.")
        if "20" not in str(rx.get("dosage", "")):
            errors.append(f"Expected dosage containing '20', got '{rx.get('dosage')}'.")

    # New Prednisone for Jessica (pat_005) → CVS (pharm_001)
    jess_pred = [
        rx for rx in state["prescriptions"]
        if rx["id"] not in seed_ids
        and rx.get("patientId") == "pat_005"
        and "prednisone" in rx.get("drugName", "").lower()
    ]
    if not jess_pred:
        errors.append("No new Prednisone prescription found for Jessica Morales.")
    else:
        rx = jess_pred[0]
        if rx.get("pharmacyId") != "pharm_001":
            errors.append(f"Expected Jessica's Prednisone at CVS (pharm_001), got '{rx.get('pharmacyId')}'.")
        if rx.get("quantity") != 5:
            errors.append(f"Expected quantity 5, got {rx.get('quantity')}.")
        if "20" not in str(rx.get("dosage", "")):
            errors.append(f"Expected dosage containing '20', got '{rx.get('dosage')}'.")

    if errors:
        return False, " ".join(errors)
    return True, "Prednisone prescribed for both William and Jessica at their respective pharmacies."
