import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."

    state = resp.json()
    prescriptions = state.get("prescriptions", [])
    seed_ids = {f"rx_{str(i).zfill(3)}" for i in range(1, 31)}

    matches = [
        rx for rx in prescriptions
        if rx.get("patientId") == "pat_001"
        and "zolpidem" in rx.get("drugName", "").lower()
        and rx.get("id") not in seed_ids
    ]

    if not matches:
        return False, "No new Zolpidem prescription found for pat_001."

    rx = matches[0]
    errors = []

    if "5mg" not in rx.get("formStrength", ""):
        errors.append(f"formStrength should contain '5mg', got '{rx.get('formStrength')}'")
    if rx.get("route") != "Oral":
        errors.append(f"route should be 'Oral', got '{rx.get('route')}'")
    if rx.get("quantity") != 30:
        errors.append(f"quantity should be 30, got {rx.get('quantity')}")
    if rx.get("daysSupply") != 30:
        errors.append(f"daysSupply should be 30, got {rx.get('daysSupply')}")
    if rx.get("refillsTotal") != 0:
        errors.append(f"refillsTotal should be 0, got {rx.get('refillsTotal')}")
    if rx.get("pharmacyId") != "pharm_001":
        errors.append(f"pharmacyId should be 'pharm_001' (CVS), got '{rx.get('pharmacyId')}'")
    if rx.get("status") != "active":
        errors.append(f"status should be 'active', got '{rx.get('status')}'")
    sig = rx.get("sig", "")
    if "bedtime" not in sig.lower():
        errors.append(f"sig should contain 'bedtime', got '{sig}'")

    if errors:
        return False, "New Zolpidem prescription found but has issues: " + "; ".join(errors)

    return True, "New Zolpidem (Schedule IV) prescription for Margaret Chen is correct."
