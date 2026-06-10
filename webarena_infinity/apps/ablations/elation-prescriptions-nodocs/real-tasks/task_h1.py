import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."

    state = resp.json()
    prescriptions = state.get("prescriptions", [])

    # Check rx_014 (Apixaban/Eliquis) is discontinued
    rx_014 = None
    for rx in prescriptions:
        if rx.get("id") == "rx_014":
            rx_014 = rx
            break

    if rx_014 is None:
        return False, "Prescription rx_014 (Apixaban/Eliquis) not found in state."

    if rx_014.get("status") != "discontinued":
        return False, f"Expected rx_014 (Eliquis) status to be 'discontinued', but got '{rx_014.get('status')}'."

    # Find new Warfarin prescription for pat_001
    seed_ids = {f"rx_{str(i).zfill(3)}" for i in range(1, 31)}
    matches = [
        rx for rx in prescriptions
        if rx["id"] not in seed_ids
        and rx.get("patientId") == "pat_001"
        and "warfarin" in rx.get("drugName", "").lower()
    ]

    if not matches:
        return False, "No new Warfarin prescription found for Margaret (pat_001)."

    new_rx = matches[0]
    errors = []

    if "5mg" not in new_rx.get("formStrength", "").lower().replace(" ", ""):
        errors.append(f"Expected formStrength to contain '5mg', got '{new_rx.get('formStrength')}'.")

    if new_rx.get("frequency") != "Once daily":
        errors.append(f"Expected frequency 'Once daily', got '{new_rx.get('frequency')}'.")

    if new_rx.get("quantity") != 30:
        errors.append(f"Expected quantity 30, got {new_rx.get('quantity')}.")

    if new_rx.get("refillsTotal") != 0:
        errors.append(f"Expected refillsTotal 0, got {new_rx.get('refillsTotal')}.")

    if new_rx.get("daw") is not True:
        errors.append(f"Expected daw to be True, got {new_rx.get('daw')}.")

    if new_rx.get("pharmacyId") != "pharm_001":
        errors.append(f"Expected pharmacyId 'pharm_001' (CVS), got '{new_rx.get('pharmacyId')}'.")

    if errors:
        return False, "New Warfarin prescription found but has issues: " + " ".join(errors)

    return True, "Eliquis discontinued and Warfarin 5mg prescribed correctly for Margaret."
