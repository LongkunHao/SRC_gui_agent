import requests


def verify(server_url: str) -> tuple[bool, str]:
    """Bulk qty change: every active oral rx with qty 30 → 60."""
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."

    state = resp.json()
    errors = []

    # Should be changed to 60: rx_002, rx_004, rx_005, rx_013
    for rx_id, name in [("rx_002", "Amlodipine"), ("rx_004", "Levothyroxine"),
                        ("rx_005", "Pantoprazole"), ("rx_013", "Sertraline")]:
        rx = next((r for r in state["prescriptions"] if r["id"] == rx_id), None)
        if not rx:
            errors.append(f"Prescription {rx_id} ({name}) not found.")
        elif rx.get("quantity") != 60:
            errors.append(f"Expected {rx_id} ({name}) quantity 60, got {rx.get('quantity')}.")

    # Should remain unchanged: rx_001 (90), rx_003 (60), rx_007 (90), rx_014 (60)
    for rx_id, name, expected_qty in [("rx_001", "Atorvastatin", 90), ("rx_003", "Metformin", 60),
                                      ("rx_007", "Gabapentin", 90), ("rx_014", "Apixaban", 60)]:
        rx = next((r for r in state["prescriptions"] if r["id"] == rx_id), None)
        if rx and rx.get("quantity") != expected_qty:
            errors.append(f"Expected {rx_id} ({name}) quantity to remain {expected_qty}, got {rx.get('quantity')}.")

    if errors:
        return False, " ".join(errors)
    return True, "All active oral prescriptions with qty 30 correctly increased to 60."
