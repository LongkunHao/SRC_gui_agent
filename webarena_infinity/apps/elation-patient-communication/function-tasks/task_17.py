import requests


def verify(server_url: str) -> tuple[bool, str]:
    """Verify Robert Washington (pat_3) has smsOptInStatus == 'opted_in'."""
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, f"Failed to fetch state: HTTP {resp.status_code}"

    state = resp.json()
    patients = state.get("patients", [])

    patient = None
    for p in patients:
        if p.get("firstName") == "Robert" and p.get("lastName") == "Washington":
            patient = p
            break

    if patient is None:
        return False, "Patient Robert Washington not found in state"

    sms_status = patient.get("smsOptInStatus")
    if sms_status != "opted_in":
        return False, f"Robert Washington smsOptInStatus is '{sms_status}', expected 'opted_in'"

    return True, "Robert Washington (pat_3) smsOptInStatus is 'opted_in'"
