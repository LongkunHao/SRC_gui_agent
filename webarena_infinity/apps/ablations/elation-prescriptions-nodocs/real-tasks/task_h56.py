import requests


def verify(server_url: str) -> tuple[bool, str]:
    """Date-based discovery: renew Margaret's active rxs started before June 2025."""
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."

    state = resp.json()
    errors = []

    # Active prescriptions for Margaret started before June 2025:
    # rx_003 (Metformin, 2025-03-10) and rx_004 (Levothyroxine, 2024-09-05)
    pre_june = {
        "rx_003": "Metformin (started 2025-03-10)",
        "rx_004": "Levothyroxine (started 2024-09-05)",
    }

    for rx_id, name in pre_june.items():
        rx = next((r for r in state["prescriptions"] if r["id"] == rx_id), None)
        if not rx:
            errors.append(f"Prescription {rx_id} ({name}) not found.")
        elif rx.get("refillsRemaining", 0) < 5:
            errors.append(f"Expected {rx_id} ({name}) refillsRemaining >= 5, got {rx.get('refillsRemaining')}.")

    if errors:
        return False, " ".join(errors)
    return True, "All pre-June-2025 active prescriptions renewed with 5 refills."
