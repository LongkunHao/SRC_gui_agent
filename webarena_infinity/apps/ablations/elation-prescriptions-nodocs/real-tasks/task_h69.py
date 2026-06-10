import requests


def verify(server_url: str) -> tuple[bool, str]:
    """Beta blocker: double Metoprolol dose, renew Carvedilol 6."""
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."

    state = resp.json()
    errors = []

    # rx_016 (David's Metoprolol 50mg) → dosage 100mg
    rx_016 = next((r for r in state["prescriptions"] if r["id"] == "rx_016"), None)
    if not rx_016:
        errors.append("Prescription rx_016 (Metoprolol) not found.")
    elif "100" not in str(rx_016.get("dosage", "")):
        errors.append(f"Expected rx_016 (Metoprolol) dosage containing '100', got '{rx_016.get('dosage')}'.")

    # rx_028 (Robert's Carvedilol) → renewed 6
    rx_028 = next((r for r in state["prescriptions"] if r["id"] == "rx_028"), None)
    if not rx_028:
        errors.append("Prescription rx_028 (Carvedilol) not found.")
    elif rx_028.get("refillsRemaining", 0) < 6:
        errors.append(f"Expected rx_028 (Carvedilol) refillsRemaining >= 6, got {rx_028.get('refillsRemaining')}.")

    if errors:
        return False, " ".join(errors)
    return True, "Beta blocker prescriptions updated correctly."
