import requests


def verify(server_url: str) -> tuple[bool, str]:
    """Diabetes audit: Metformin → qty 90, non-Metformin diabetes meds → renew 5."""
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."

    state = resp.json()
    errors = []

    # rx_003 (Margaret's Metformin 1000mg) → qty 90
    rx_003 = next((r for r in state["prescriptions"] if r["id"] == "rx_003"), None)
    if not rx_003:
        errors.append("Prescription rx_003 (Margaret's Metformin) not found.")
    elif rx_003.get("quantity") != 90:
        errors.append(f"Expected rx_003 (Metformin) quantity 90, got {rx_003.get('quantity')}.")

    # rx_019 (David's Metformin ER 500mg) → qty 90
    rx_019 = next((r for r in state["prescriptions"] if r["id"] == "rx_019"), None)
    if not rx_019:
        errors.append("Prescription rx_019 (David's Metformin ER) not found.")
    elif rx_019.get("quantity") != 90:
        errors.append(f"Expected rx_019 (Metformin ER) quantity 90, got {rx_019.get('quantity')}.")

    # rx_023 (William's Insulin Glargine) → renewed 5
    rx_023 = next((r for r in state["prescriptions"] if r["id"] == "rx_023"), None)
    if not rx_023:
        errors.append("Prescription rx_023 (Insulin Glargine) not found.")
    elif rx_023.get("refillsRemaining", 0) < 5:
        errors.append(f"Expected rx_023 (Insulin) refillsRemaining >= 5, got {rx_023.get('refillsRemaining')}.")

    # rx_027 (Robert's Empagliflozin) → renewed 5
    rx_027 = next((r for r in state["prescriptions"] if r["id"] == "rx_027"), None)
    if not rx_027:
        errors.append("Prescription rx_027 (Empagliflozin) not found.")
    elif rx_027.get("refillsRemaining", 0) < 5:
        errors.append(f"Expected rx_027 (Empagliflozin) refillsRemaining >= 5, got {rx_027.get('refillsRemaining')}.")

    if errors:
        return False, " ".join(errors)
    return True, "Diabetes medication audit completed correctly."
