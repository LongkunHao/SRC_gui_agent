import requests


def verify(server_url: str) -> tuple[bool, str]:
    """Margaret's non-Mitchell 2025 prescriptions → renew 5 each."""
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."

    state = resp.json()
    errors = []

    # rx_007 (Gabapentin, by Dr. Reyes, 2025-12-01) → renewed 5
    rx_007 = next((r for r in state["prescriptions"] if r["id"] == "rx_007"), None)
    if not rx_007:
        errors.append("Prescription rx_007 (Gabapentin) not found.")
    elif rx_007.get("refillsRemaining", 0) < 5:
        errors.append(f"Expected rx_007 (Gabapentin) refillsRemaining >= 5, got {rx_007.get('refillsRemaining')}.")

    # rx_014 (Apixaban, by Dr. Tanaka, 2025-11-20) → renewed 5
    rx_014 = next((r for r in state["prescriptions"] if r["id"] == "rx_014"), None)
    if not rx_014:
        errors.append("Prescription rx_014 (Apixaban) not found.")
    elif rx_014.get("refillsRemaining", 0) < 5:
        errors.append(f"Expected rx_014 (Apixaban) refillsRemaining >= 5, got {rx_014.get('refillsRemaining')}.")

    if errors:
        return False, " ".join(errors)
    return True, "Margaret's non-Mitchell 2025 prescriptions renewed correctly."
