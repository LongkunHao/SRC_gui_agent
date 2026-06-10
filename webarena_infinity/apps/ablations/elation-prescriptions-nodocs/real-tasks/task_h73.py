import requests


def verify(server_url: str) -> tuple[bool, str]:
    """Dual-patient Fluconazole + Jessica medication management."""
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."

    state = resp.json()
    errors = []
    seed_ids = {f"rx_{str(i).zfill(3)}" for i in range(1, 31)}

    # New Fluconazole for Aisha (pat_003) → Walgreens
    aisha_flu = [
        rx for rx in state["prescriptions"]
        if rx["id"] not in seed_ids
        and rx.get("patientId") == "pat_003"
        and "fluconazole" in rx.get("drugName", "").lower()
    ]
    if not aisha_flu:
        errors.append("No new Fluconazole prescription found for Aisha Rahman.")
    else:
        rx = aisha_flu[0]
        if rx.get("pharmacyId") != "pharm_002":
            errors.append(f"Expected Aisha's Fluconazole at Walgreens (pharm_002), got '{rx.get('pharmacyId')}'.")
        if rx.get("quantity") != 1:
            errors.append(f"Expected Aisha's Fluconazole quantity 1, got {rx.get('quantity')}.")

    # New Fluconazole for Jessica (pat_005) → CVS
    jess_flu = [
        rx for rx in state["prescriptions"]
        if rx["id"] not in seed_ids
        and rx.get("patientId") == "pat_005"
        and "fluconazole" in rx.get("drugName", "").lower()
    ]
    if not jess_flu:
        errors.append("No new Fluconazole prescription found for Jessica Morales.")
    else:
        rx = jess_flu[0]
        if rx.get("pharmacyId") != "pharm_001":
            errors.append(f"Expected Jessica's Fluconazole at CVS (pharm_001), got '{rx.get('pharmacyId')}'.")
        if rx.get("quantity") != 1:
            errors.append(f"Expected Jessica's Fluconazole quantity 1, got {rx.get('quantity')}.")

    # rx_025 (Cephalexin) → discontinued
    rx_025 = next((r for r in state["prescriptions"] if r["id"] == "rx_025"), None)
    if not rx_025:
        errors.append("Prescription rx_025 (Cephalexin) not found.")
    elif rx_025.get("status") != "discontinued":
        errors.append(f"Expected rx_025 (Cephalexin) status 'discontinued', got '{rx_025.get('status')}'.")

    # rx_026 (Fluoxetine) → renewed 5
    rx_026 = next((r for r in state["prescriptions"] if r["id"] == "rx_026"), None)
    if not rx_026:
        errors.append("Prescription rx_026 (Fluoxetine) not found.")
    elif rx_026.get("refillsRemaining", 0) < 5:
        errors.append(f"Expected rx_026 (Fluoxetine) refillsRemaining >= 5, got {rx_026.get('refillsRemaining')}.")

    if errors:
        return False, " ".join(errors)
    return True, "Dual Fluconazole prescribed, Cephalexin discontinued, Fluoxetine renewed."
