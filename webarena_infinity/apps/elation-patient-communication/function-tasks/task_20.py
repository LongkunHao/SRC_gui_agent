import requests


def verify(server_url: str) -> tuple[bool, str]:
    """Verify Kevin Adebayo (pat_11) has emergencyContact with name 'Grace Adebayo', phone '(650) 555-1122', relationship 'Wife'."""
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, f"Failed to fetch state: HTTP {resp.status_code}"

    state = resp.json()
    patients = state.get("patients", [])

    patient = None
    for p in patients:
        if p.get("firstName") == "Kevin" and p.get("lastName") == "Adebayo":
            patient = p
            break

    if patient is None:
        return False, "Patient Kevin Adebayo not found in state"

    ec = patient.get("emergencyContact")
    if ec is None:
        return False, "Kevin Adebayo emergencyContact is None, expected contact info"

    if ec.get("name") != "Grace Adebayo":
        return False, f"emergencyContact name is '{ec.get('name')}', expected 'Grace Adebayo'"

    if ec.get("phone") != "(650) 555-1122":
        return False, f"emergencyContact phone is '{ec.get('phone')}', expected '(650) 555-1122'"

    if ec.get("relationship") != "Wife":
        return False, f"emergencyContact relationship is '{ec.get('relationship')}', expected 'Wife'"

    return True, "Kevin Adebayo (pat_11) emergencyContact is Grace Adebayo, (650) 555-1122, Wife"
