import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."

    state = resp.json()

    # Check current patient is Jessica Morales
    if state.get("currentPatientId") != "pat_005":
        return False, f"Expected currentPatientId 'pat_005' (Jessica Morales), got '{state.get('currentPatientId')}'."

    prescriptions = state.get("prescriptions", [])
    errors = []

    # Check rx_025 (Cephalexin) is discontinued
    rx_025 = None
    for rx in prescriptions:
        if rx.get("id") == "rx_025":
            rx_025 = rx
            break

    if rx_025 is None:
        errors.append("Prescription rx_025 (Cephalexin) not found.")
    elif rx_025.get("status") != "discontinued":
        errors.append(f"Expected rx_025 (Cephalexin) status 'discontinued', got '{rx_025.get('status')}'.")

    # Check rx_026 (Fluoxetine) renewed with 5 refills
    rx_026 = None
    for rx in prescriptions:
        if rx.get("id") == "rx_026":
            rx_026 = rx
            break

    if rx_026 is None:
        errors.append("Prescription rx_026 (Fluoxetine) not found.")
    else:
        if rx_026.get("refillsRemaining") != 5:
            errors.append(f"Expected rx_026 (Fluoxetine) refillsRemaining 5, got {rx_026.get('refillsRemaining')}.")
        if rx_026.get("refillsTotal") != 5:
            errors.append(f"Expected rx_026 (Fluoxetine) refillsTotal 5, got {rx_026.get('refillsTotal')}.")
        if rx_026.get("status") != "active":
            errors.append(f"Expected rx_026 (Fluoxetine) status 'active', got '{rx_026.get('status')}'.")

    if errors:
        return False, " ".join(errors)

    return True, "Cephalexin discontinued and Fluoxetine renewed with 5 refills for Jessica Morales."
