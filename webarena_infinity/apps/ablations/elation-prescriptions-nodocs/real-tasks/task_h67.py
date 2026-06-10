import requests


def verify(server_url: str) -> tuple[bool, str]:
    """Dr. Tanaka audit: hold PA rxs, renew non-PA with 5."""
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."

    state = resp.json()
    errors = []

    # rx_014 (Apixaban, PA=true) → on-hold
    rx_014 = next((r for r in state["prescriptions"] if r["id"] == "rx_014"), None)
    if not rx_014:
        errors.append("Prescription rx_014 (Apixaban) not found.")
    elif rx_014.get("status") != "on-hold":
        errors.append(f"Expected rx_014 (Apixaban) status 'on-hold', got '{rx_014.get('status')}'.")

    # rx_024 (Furosemide, no PA) → renewed 5
    rx_024 = next((r for r in state["prescriptions"] if r["id"] == "rx_024"), None)
    if not rx_024:
        errors.append("Prescription rx_024 (Furosemide) not found.")
    elif rx_024.get("refillsRemaining", 0) < 5:
        errors.append(f"Expected rx_024 (Furosemide) refillsRemaining >= 5, got {rx_024.get('refillsRemaining')}.")

    # rx_028 (Carvedilol, no PA) → renewed 5
    rx_028 = next((r for r in state["prescriptions"] if r["id"] == "rx_028"), None)
    if not rx_028:
        errors.append("Prescription rx_028 (Carvedilol) not found.")
    elif rx_028.get("refillsRemaining", 0) < 5:
        errors.append(f"Expected rx_028 (Carvedilol) refillsRemaining >= 5, got {rx_028.get('refillsRemaining')}.")

    # rx_029 (Spironolactone, no PA) → renewed 5
    rx_029 = next((r for r in state["prescriptions"] if r["id"] == "rx_029"), None)
    if not rx_029:
        errors.append("Prescription rx_029 (Spironolactone) not found.")
    elif rx_029.get("refillsRemaining", 0) < 5:
        errors.append(f"Expected rx_029 (Spironolactone) refillsRemaining >= 5, got {rx_029.get('refillsRemaining')}.")

    if errors:
        return False, " ".join(errors)
    return True, "Dr. Tanaka audit completed — PA prescriptions held, others renewed."
