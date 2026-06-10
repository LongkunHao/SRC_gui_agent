import requests


def verify(server_url: str) -> tuple[bool, str]:
    """SSRI→SNRI switch: deny Sertraline refill, discontinue, prescribe Duloxetine."""
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."

    state = resp.json()
    errors = []
    seed_ids = {f"rx_{str(i).zfill(3)}" for i in range(1, 31)}

    # rr_011 (Sertraline refill) → denied
    rr_011 = next((r for r in state["refillRequests"] if r["id"] == "rr_011"), None)
    if not rr_011:
        errors.append("Refill request rr_011 (Sertraline) not found.")
    elif rr_011.get("status") != "denied":
        errors.append(f"Expected rr_011 (Sertraline) status 'denied', got '{rr_011.get('status')}'.")

    # rx_013 (Sertraline) → discontinued
    rx_013 = next((r for r in state["prescriptions"] if r["id"] == "rx_013"), None)
    if not rx_013:
        errors.append("Prescription rx_013 (Sertraline) not found.")
    elif rx_013.get("status") != "discontinued":
        errors.append(f"Expected rx_013 (Sertraline) status 'discontinued', got '{rx_013.get('status')}'.")

    # New Duloxetine for Margaret
    new_dul = [
        rx for rx in state["prescriptions"]
        if rx["id"] not in seed_ids
        and rx.get("patientId") == "pat_001"
        and "duloxetine" in rx.get("drugName", "").lower()
    ]
    if not new_dul:
        errors.append("No new Duloxetine prescription found for Margaret Chen.")
    else:
        rx = new_dul[0]
        if "60" not in str(rx.get("dosage", "")):
            errors.append(f"Expected Duloxetine dosage containing '60', got '{rx.get('dosage')}'.")
        if rx.get("pharmacyId") != "pharm_001":
            errors.append(f"Expected Duloxetine pharmacyId 'pharm_001' (CVS), got '{rx.get('pharmacyId')}'.")
        if rx.get("quantity") != 30:
            errors.append(f"Expected Duloxetine quantity 30, got {rx.get('quantity')}.")
        if rx.get("refillsTotal", 0) < 3:
            errors.append(f"Expected Duloxetine refillsTotal >= 3, got {rx.get('refillsTotal')}.")

    if errors:
        return False, " ".join(errors)
    return True, "Sertraline-to-Duloxetine switch completed correctly."
