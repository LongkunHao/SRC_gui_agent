import requests


def verify(server_url: str) -> tuple[bool, str]:
    """Discovery: statin+beta-blocker patient → modify both."""
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."

    state = resp.json()
    errors = []

    # David (pat_002) has both statin (Atorvastatin) and beta-blocker (Metoprolol)
    # rx_017 (Atorvastatin) → dosage 80mg
    rx_017 = next((r for r in state["prescriptions"] if r["id"] == "rx_017"), None)
    if not rx_017:
        errors.append("Prescription rx_017 (Atorvastatin) not found.")
    elif "80" not in str(rx_017.get("dosage", "")):
        errors.append(f"Expected rx_017 (Atorvastatin) dosage containing '80', got '{rx_017.get('dosage')}'.")

    # rx_016 (Metoprolol) → quantity 60
    rx_016 = next((r for r in state["prescriptions"] if r["id"] == "rx_016"), None)
    if not rx_016:
        errors.append("Prescription rx_016 (Metoprolol) not found.")
    elif rx_016.get("quantity") != 60:
        errors.append(f"Expected rx_016 (Metoprolol) quantity 60, got {rx_016.get('quantity')}.")

    # Should be on David's chart
    if state.get("currentPatientId") != "pat_002":
        errors.append(f"Expected currentPatientId 'pat_002' (David Kowalski), got '{state.get('currentPatientId')}'.")

    if errors:
        return False, " ".join(errors)
    return True, "Statin and beta-blocker patient found, both prescriptions modified."
