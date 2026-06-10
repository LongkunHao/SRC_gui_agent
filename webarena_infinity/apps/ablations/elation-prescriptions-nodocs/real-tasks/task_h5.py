import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."

    state = resp.json()
    prescriptions = state.get("prescriptions", [])
    errors = []

    # Check rx_005 (Pantoprazole 40mg) is discontinued
    rx_005 = None
    for rx in prescriptions:
        if rx.get("id") == "rx_005":
            rx_005 = rx
            break

    if rx_005 is None:
        errors.append("Prescription rx_005 (Pantoprazole 40mg) not found.")
    elif rx_005.get("status") != "discontinued":
        errors.append(f"Expected rx_005 (Pantoprazole 40mg) status 'discontinued', got '{rx_005.get('status')}'.")

    # Find new Pantoprazole 20mg prescription for pat_001
    seed_ids = {f"rx_{str(i).zfill(3)}" for i in range(1, 31)}
    matches = [
        rx for rx in prescriptions
        if rx["id"] not in seed_ids
        and rx.get("patientId") == "pat_001"
        and "pantoprazole" in rx.get("drugName", "").lower()
        and "20mg" in rx.get("formStrength", "").lower().replace(" ", "")
    ]

    if not matches:
        errors.append("No new Pantoprazole 20mg prescription found for Margaret (pat_001).")
    else:
        new_rx = matches[0]
        if new_rx.get("quantity") != 30:
            errors.append(f"New Pantoprazole: expected quantity 30, got {new_rx.get('quantity')}.")
        if new_rx.get("daysSupply") != 30:
            errors.append(f"New Pantoprazole: expected daysSupply 30, got {new_rx.get('daysSupply')}.")
        if new_rx.get("refillsTotal") != 2:
            errors.append(f"New Pantoprazole: expected refillsTotal 2, got {new_rx.get('refillsTotal')}.")
        if new_rx.get("pharmacyId") != "pharm_001":
            errors.append(f"New Pantoprazole: expected pharmacyId 'pharm_001' (CVS), got '{new_rx.get('pharmacyId')}'.")

    if errors:
        return False, " ".join(errors)

    return True, "Pantoprazole 40mg discontinued and Pantoprazole 20mg prescribed correctly for Margaret."
