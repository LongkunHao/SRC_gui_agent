import requests


def verify(server_url: str) -> tuple[bool, str]:
    """3-patient: David hold Metoprolol, William renew Valsartan 5, Jessica discontinue Cephalexin."""
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."

    state = resp.json()
    errors = []

    # rx_016 (David's Metoprolol) → on-hold
    rx_016 = next((r for r in state["prescriptions"] if r["id"] == "rx_016"), None)
    if not rx_016:
        errors.append("Prescription rx_016 (Metoprolol) not found.")
    elif rx_016.get("status") != "on-hold":
        errors.append(f"Expected rx_016 (Metoprolol) status 'on-hold', got '{rx_016.get('status')}'.")

    # rx_022 (William's Valsartan) → renewed with 5 refills
    rx_022 = next((r for r in state["prescriptions"] if r["id"] == "rx_022"), None)
    if not rx_022:
        errors.append("Prescription rx_022 (Valsartan) not found.")
    elif rx_022.get("refillsRemaining", 0) < 5:
        errors.append(f"Expected rx_022 (Valsartan) refillsRemaining >= 5, got {rx_022.get('refillsRemaining')}.")

    # rx_025 (Jessica's Cephalexin) → discontinued
    rx_025 = next((r for r in state["prescriptions"] if r["id"] == "rx_025"), None)
    if not rx_025:
        errors.append("Prescription rx_025 (Cephalexin) not found.")
    elif rx_025.get("status") != "discontinued":
        errors.append(f"Expected rx_025 (Cephalexin) status 'discontinued', got '{rx_025.get('status')}'.")

    # End on Jessica's chart
    if state.get("currentPatientId") != "pat_005":
        errors.append(f"Expected currentPatientId 'pat_005' (Jessica Morales), got '{state.get('currentPatientId')}'.")

    if errors:
        return False, " ".join(errors)
    return True, "Three-patient workflow completed correctly."
