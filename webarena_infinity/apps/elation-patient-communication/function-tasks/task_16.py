import requests


def verify(server_url: str) -> tuple[bool, str]:
    """Verify David Park (pat_7) has smsOptInStatus == 'opted_out'."""
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, f"Failed to fetch state: HTTP {resp.status_code}"

    state = resp.json()
    patients = state.get("patients", [])

    patient = None
    for p in patients:
        if p.get("firstName") == "David" and p.get("lastName") == "Park":
            patient = p
            break

    if patient is None:
        return False, "Patient David Park not found in state"

    sms_status = patient.get("smsOptInStatus")
    if sms_status != "opted_out":
        return False, f"David Park smsOptInStatus is '{sms_status}', expected 'opted_out'"

    return True, "David Park (pat_7) smsOptInStatus is 'opted_out'"
