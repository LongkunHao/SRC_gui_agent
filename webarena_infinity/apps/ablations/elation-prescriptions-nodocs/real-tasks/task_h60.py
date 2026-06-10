import requests


def verify(server_url: str) -> tuple[bool, str]:
    """End-of-shift: deny Atorvastatin refill, modify Metformin refill, William Furosemide 80mg, Jessica Fluoxetine renew, remove Ibuprofen from favorites."""
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."

    state = resp.json()
    errors = []

    # rr_001 (Atorvastatin) -> denied
    rr_001 = next((r for r in state["refillRequests"] if r["id"] == "rr_001"), None)
    if not rr_001:
        errors.append("Refill request rr_001 not found.")
    elif rr_001.get("status") != "denied":
        errors.append(f"Expected rr_001 (Atorvastatin) status 'denied', got '{rr_001.get('status')}'.")

    # rr_002 (Metformin) -> modified
    rr_002 = next((r for r in state["refillRequests"] if r["id"] == "rr_002"), None)
    if not rr_002:
        errors.append("Refill request rr_002 not found.")
    elif rr_002.get("status") != "modified":
        errors.append(f"Expected rr_002 (Metformin) status 'modified', got '{rr_002.get('status')}'.")
    elif not rr_002.get("modifiedDetails"):
        errors.append("Expected rr_002 to have modifiedDetails.")

    # rx_024 (William's Furosemide) -> dosage 80mg
    rx_024 = next((r for r in state["prescriptions"] if r["id"] == "rx_024"), None)
    if not rx_024:
        errors.append("Prescription rx_024 (Furosemide) not found.")
    elif "80" not in str(rx_024.get("dosage", "")):
        errors.append(f"Expected rx_024 (Furosemide) dosage containing '80', got '{rx_024.get('dosage')}'.")

    # rx_026 (Jessica's Fluoxetine) -> renewed with 6 refills
    rx_026 = next((r for r in state["prescriptions"] if r["id"] == "rx_026"), None)
    if not rx_026:
        errors.append("Prescription rx_026 (Fluoxetine) not found.")
    elif rx_026.get("refillsRemaining", 0) < 6:
        errors.append(f"Expected rx_026 (Fluoxetine) refillsRemaining >= 6, got {rx_026.get('refillsRemaining')}.")

    # Ibuprofen removed from favorites
    favs = state.get("settings", {}).get("favoritesDrugIds", [])
    if "drug_043" in favs:
        errors.append("Ibuprofen (drug_043) is still in favorites.")

    if errors:
        return False, " ".join(errors)
    return True, "End-of-shift tasks completed correctly."
