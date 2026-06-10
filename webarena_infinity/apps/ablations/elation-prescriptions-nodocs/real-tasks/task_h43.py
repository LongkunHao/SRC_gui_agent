import requests


def verify(server_url: str) -> tuple[bool, str]:
    """Dr. Okafor's prescriptions all renewed with 4 refills."""
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."

    state = resp.json()
    errors = []

    # Dr. Okafor (prov_002) wrote these active prescriptions:
    okafor_rxs = {
        "rx_004": "Levothyroxine (Margaret)",
        "rx_018": "Escitalopram (David)",
        "rx_021": "Escitalopram (Aisha)",
        "rx_026": "Fluoxetine (Jessica)",
    }

    for rx_id, name in okafor_rxs.items():
        rx = next((r for r in state["prescriptions"] if r["id"] == rx_id), None)
        if not rx:
            errors.append(f"Prescription {rx_id} ({name}) not found.")
        elif rx.get("refillsRemaining", 0) < 4:
            errors.append(f"Expected {rx_id} ({name}) refillsRemaining >= 4, got {rx.get('refillsRemaining')}.")

    if errors:
        return False, " ".join(errors)
    return True, "All of Dr. Okafor's prescriptions renewed with 4 refills."
