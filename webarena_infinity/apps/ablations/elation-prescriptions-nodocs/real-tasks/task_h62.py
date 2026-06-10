import requests


def verify(server_url: str) -> tuple[bool, str]:
    """Cross-patient Escitalopram: fewer refills → renew 6, other → dosage 20mg."""
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."

    state = resp.json()
    errors = []

    # rx_018 (David's Escitalopram, had 2 refills) → renewed to 6
    rx_018 = next((r for r in state["prescriptions"] if r["id"] == "rx_018"), None)
    if not rx_018:
        errors.append("Prescription rx_018 (David's Escitalopram) not found.")
    elif rx_018.get("refillsRemaining", 0) < 6:
        errors.append(f"Expected rx_018 (David's Escitalopram) refillsRemaining >= 6, got {rx_018.get('refillsRemaining')}.")

    # rx_021 (Aisha's Escitalopram, had 5 refills) → dosage 20mg
    rx_021 = next((r for r in state["prescriptions"] if r["id"] == "rx_021"), None)
    if not rx_021:
        errors.append("Prescription rx_021 (Aisha's Escitalopram) not found.")
    elif "20" not in str(rx_021.get("dosage", "")):
        errors.append(f"Expected rx_021 (Aisha's Escitalopram) dosage containing '20', got '{rx_021.get('dosage')}'.")

    if errors:
        return False, " ".join(errors)
    return True, "Escitalopram prescriptions correctly updated — renewed lower-refill, increased dosage on other."
