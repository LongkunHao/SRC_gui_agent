import requests


def verify(server_url: str) -> tuple[bool, str]:
    """Specialty pharmacy switch: discontinue Semaglutide at BioPlus, represcribe at Accredo."""
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."

    state = resp.json()
    errors = []
    seed_ids = {f"rx_{str(i).zfill(3)}" for i in range(1, 31)}

    # rx_030 (Semaglutide at BioPlus) → discontinued
    rx_030 = next((r for r in state["prescriptions"] if r["id"] == "rx_030"), None)
    if not rx_030:
        errors.append("Prescription rx_030 (Semaglutide at BioPlus) not found.")
    elif rx_030.get("status") != "discontinued":
        errors.append(f"Expected rx_030 status 'discontinued', got '{rx_030.get('status')}'.")

    # New Semaglutide at Accredo
    new_sema = [
        rx for rx in state["prescriptions"]
        if rx["id"] not in seed_ids
        and rx.get("patientId") == "pat_001"
        and "semaglutide" in rx.get("drugName", "").lower()
    ]
    if not new_sema:
        errors.append("No new Semaglutide prescription found for Margaret at Accredo.")
    else:
        rx = new_sema[0]
        if rx.get("pharmacyId") != "pharm_011":
            errors.append(f"Expected pharmacyId 'pharm_011' (Accredo), got '{rx.get('pharmacyId')}'.")
        if rx.get("frequency") != "Once weekly":
            errors.append(f"Expected frequency 'Once weekly', got '{rx.get('frequency')}'.")
        if rx.get("route") != "Subcutaneous":
            errors.append(f"Expected route 'Subcutaneous', got '{rx.get('route')}'.")
        if rx.get("quantity") != 1:
            errors.append(f"Expected quantity 1, got {rx.get('quantity')}.")
        if rx.get("daysSupply") != 28:
            errors.append(f"Expected daysSupply 28, got {rx.get('daysSupply')}.")
        if rx.get("refillsTotal", 0) < 3:
            errors.append(f"Expected refillsTotal >= 3, got {rx.get('refillsTotal')}.")
        if not rx.get("priorAuth"):
            errors.append("Expected priorAuth to be true.")
        pa_num = rx.get("priorAuthNumber", "")
        if "12345" not in str(pa_num):
            errors.append(f"Expected priorAuthNumber containing '12345', got '{pa_num}'.")

    if errors:
        return False, " ".join(errors)
    return True, "Semaglutide moved from BioPlus to Accredo with prior authorization."
