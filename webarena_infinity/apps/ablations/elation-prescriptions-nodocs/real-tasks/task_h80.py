import requests


def verify(server_url: str) -> tuple[bool, str]:
    """Grand weekly review: Margaret mods, David qty, Robert hold+renew."""
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."

    state = resp.json()
    errors = []

    # rx_002 (Margaret's Amlodipine) → dosage 10mg
    rx_002 = next((r for r in state["prescriptions"] if r["id"] == "rx_002"), None)
    if not rx_002:
        errors.append("Prescription rx_002 (Amlodipine) not found.")
    elif "10" not in str(rx_002.get("dosage", "")):
        errors.append(f"Expected rx_002 (Amlodipine) dosage containing '10', got '{rx_002.get('dosage')}'.")

    # rx_014 (Margaret's Apixaban) → renewed 5
    rx_014 = next((r for r in state["prescriptions"] if r["id"] == "rx_014"), None)
    if not rx_014:
        errors.append("Prescription rx_014 (Apixaban) not found.")
    elif rx_014.get("refillsRemaining", 0) < 5:
        errors.append(f"Expected rx_014 (Apixaban) refillsRemaining >= 5, got {rx_014.get('refillsRemaining')}.")

    # rx_017 (David's Atorvastatin) → qty 90
    rx_017 = next((r for r in state["prescriptions"] if r["id"] == "rx_017"), None)
    if not rx_017:
        errors.append("Prescription rx_017 (David's Atorvastatin) not found.")
    elif rx_017.get("quantity") != 90:
        errors.append(f"Expected rx_017 (Atorvastatin) quantity 90, got {rx_017.get('quantity')}.")

    # rx_028 (Robert's Carvedilol) → on-hold
    rx_028 = next((r for r in state["prescriptions"] if r["id"] == "rx_028"), None)
    if not rx_028:
        errors.append("Prescription rx_028 (Carvedilol) not found.")
    elif rx_028.get("status") != "on-hold":
        errors.append(f"Expected rx_028 (Carvedilol) status 'on-hold', got '{rx_028.get('status')}'.")

    # rx_029 (Robert's Spironolactone) → renewed 4
    rx_029 = next((r for r in state["prescriptions"] if r["id"] == "rx_029"), None)
    if not rx_029:
        errors.append("Prescription rx_029 (Spironolactone) not found.")
    elif rx_029.get("refillsRemaining", 0) < 4:
        errors.append(f"Expected rx_029 (Spironolactone) refillsRemaining >= 4, got {rx_029.get('refillsRemaining')}.")

    # End on Robert's chart
    if state.get("currentPatientId") != "pat_006":
        errors.append(f"Expected currentPatientId 'pat_006' (Robert Fitzgerald), got '{state.get('currentPatientId')}'.")

    if errors:
        return False, " ".join(errors)
    return True, "Weekly review completed — prescriptions updated across three patients."
