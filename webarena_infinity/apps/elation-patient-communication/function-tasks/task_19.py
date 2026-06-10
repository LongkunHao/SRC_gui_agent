import requests


def verify(server_url: str) -> tuple[bool, str]:
    """Verify Alice Johansson (pat_34) has cellPhone == '(415) 555-9999'."""
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, f"Failed to fetch state: HTTP {resp.status_code}"

    state = resp.json()
    patients = state.get("patients", [])

    patient = None
    for p in patients:
        if p.get("firstName") == "Alice" and p.get("lastName") == "Johansson":
            patient = p
            break

    if patient is None:
        return False, "Patient Alice Johansson not found in state"

    cell_phone = patient.get("cellPhone")
    if cell_phone != "(415) 555-9999":
        return False, f"Alice Johansson cellPhone is '{cell_phone}', expected '(415) 555-9999'"

    return True, "Alice Johansson (pat_34) cellPhone is '(415) 555-9999'"
