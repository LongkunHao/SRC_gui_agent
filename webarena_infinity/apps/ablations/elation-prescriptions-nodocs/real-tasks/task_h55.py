import requests


def verify(server_url: str) -> tuple[bool, str]:
    """Atorvastatin sync: both patients at 40mg, both quantity 90."""
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."

    state = resp.json()
    errors = []

    # rx_001 Margaret's Atorvastatin -> dosage 40mg, quantity 90
    rx_001 = next((r for r in state["prescriptions"] if r["id"] == "rx_001"), None)
    if not rx_001:
        errors.append("Prescription rx_001 (Margaret's Atorvastatin) not found.")
    else:
        if "40" not in str(rx_001.get("dosage", "")):
            errors.append(f"Expected rx_001 dosage containing '40', got '{rx_001.get('dosage')}'.")
        if rx_001.get("quantity") != 90:
            errors.append(f"Expected rx_001 quantity 90, got {rx_001.get('quantity')}.")

    # rx_017 David's Atorvastatin -> dosage 40mg, quantity 90
    rx_017 = next((r for r in state["prescriptions"] if r["id"] == "rx_017"), None)
    if not rx_017:
        errors.append("Prescription rx_017 (David's Atorvastatin) not found.")
    else:
        if "40" not in str(rx_017.get("dosage", "")):
            errors.append(f"Expected rx_017 dosage containing '40', got '{rx_017.get('dosage')}'.")
        if rx_017.get("quantity") != 90:
            errors.append(f"Expected rx_017 quantity 90, got {rx_017.get('quantity')}.")

    if errors:
        return False, " ".join(errors)
    return True, "Both Atorvastatin prescriptions synchronized to 40mg, quantity 90."
