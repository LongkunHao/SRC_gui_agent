import requests


def verify(server_url: str) -> tuple[bool, str]:
    """SSRI refill check: renew those with <3 refills remaining (6 refills), leave others."""
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."

    state = resp.json()
    errors = []

    # rx_018 David's Escitalopram — had 2 refills, should be renewed to 6
    rx_018 = next((r for r in state["prescriptions"] if r["id"] == "rx_018"), None)
    if not rx_018:
        errors.append("Prescription rx_018 (David's Escitalopram) not found.")
    elif rx_018.get("refillsRemaining", 0) < 6:
        errors.append(f"Expected rx_018 (David's Escitalopram) refillsRemaining >= 6, got {rx_018.get('refillsRemaining')}.")

    # rx_026 Jessica's Fluoxetine — had 1 refill, should be renewed to 6
    rx_026 = next((r for r in state["prescriptions"] if r["id"] == "rx_026"), None)
    if not rx_026:
        errors.append("Prescription rx_026 (Jessica's Fluoxetine) not found.")
    elif rx_026.get("refillsRemaining", 0) < 6:
        errors.append(f"Expected rx_026 (Jessica's Fluoxetine) refillsRemaining >= 6, got {rx_026.get('refillsRemaining')}.")

    # rx_013 Margaret's Sertraline — had 3 refills, should be unchanged
    rx_013 = next((r for r in state["prescriptions"] if r["id"] == "rx_013"), None)
    if not rx_013:
        errors.append("Prescription rx_013 (Margaret's Sertraline) not found.")
    elif rx_013.get("refillsRemaining") != 3:
        errors.append(f"Expected rx_013 (Margaret's Sertraline) refillsRemaining to remain 3, got {rx_013.get('refillsRemaining')}.")

    # rx_021 Aisha's Escitalopram — had 5 refills, should be unchanged
    rx_021 = next((r for r in state["prescriptions"] if r["id"] == "rx_021"), None)
    if not rx_021:
        errors.append("Prescription rx_021 (Aisha's Escitalopram) not found.")
    elif rx_021.get("refillsRemaining") != 5:
        errors.append(f"Expected rx_021 (Aisha's Escitalopram) refillsRemaining to remain 5, got {rx_021.get('refillsRemaining')}.")

    if errors:
        return False, " ".join(errors)
    return True, "SSRI refill check completed correctly — renewed those with <3 refills, left others unchanged."
