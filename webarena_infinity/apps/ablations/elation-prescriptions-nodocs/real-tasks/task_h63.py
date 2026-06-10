import requests


def verify(server_url: str) -> tuple[bool, str]:
    """Cross-patient PPI: step down Margaret's Pantoprazole, prescribe Omeprazole for Aisha."""
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."

    state = resp.json()
    errors = []
    seed_ids = {f"rx_{str(i).zfill(3)}" for i in range(1, 31)}

    # rx_005 (Pantoprazole) → dosage stepped down to 20mg
    rx_005 = next((r for r in state["prescriptions"] if r["id"] == "rx_005"), None)
    if not rx_005:
        errors.append("Prescription rx_005 (Pantoprazole) not found.")
    elif "20" not in str(rx_005.get("dosage", "")):
        errors.append(f"Expected rx_005 (Pantoprazole) dosage containing '20', got '{rx_005.get('dosage')}'.")

    # New Omeprazole for Aisha (pat_003)
    new_ome = [
        rx for rx in state["prescriptions"]
        if rx["id"] not in seed_ids
        and rx.get("patientId") == "pat_003"
        and "omeprazole" in rx.get("drugName", "").lower()
    ]
    if not new_ome:
        errors.append("No new Omeprazole prescription found for Aisha Rahman.")
    else:
        rx = new_ome[0]
        if "20" not in str(rx.get("dosage", "")):
            errors.append(f"Expected new Omeprazole dosage containing '20', got '{rx.get('dosage')}'.")
        if rx.get("pharmacyId") != "pharm_002":
            errors.append(f"Expected new Omeprazole pharmacyId 'pharm_002' (Walgreens), got '{rx.get('pharmacyId')}'.")
        if rx.get("quantity") != 30:
            errors.append(f"Expected quantity 30, got {rx.get('quantity')}.")
        if rx.get("refillsTotal", 0) < 3:
            errors.append(f"Expected refillsTotal >= 3, got {rx.get('refillsTotal')}.")

    if errors:
        return False, " ".join(errors)
    return True, "PPI management completed — Pantoprazole stepped down, Omeprazole prescribed for Aisha."
