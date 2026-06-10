import requests


def verify(server_url: str) -> tuple[bool, str]:
    """Verify William Chang (pat_13) passport invitation was resent."""
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, f"Failed to fetch state: HTTP {resp.status_code}"

    state = resp.json()
    patients = state.get("patients", [])

    patient = None
    for p in patients:
        if p.get("firstName") == "William" and p.get("lastName") == "Chang":
            patient = p
            break

    if patient is None:
        return False, "Patient William Chang not found in patients"

    if patient.get("passportStatus") != "invited":
        return False, f"William Chang passportStatus is '{patient.get('passportStatus')}', expected 'invited'"

    if patient.get("invitedAt") == "2026-02-01T09:00:00Z":
        return False, "William Chang invitedAt is still the original seed value '2026-02-01T09:00:00Z', expected it to be updated after resend"

    if patient.get("invitedAt") is None:
        return False, "William Chang invitedAt is None, expected a new timestamp after resend"

    if patient.get("invitationCode") == "1746290":
        return False, "William Chang invitationCode is still the original seed value '1746290', expected a new code after resend"

    if patient.get("invitationCode") is None:
        return False, "William Chang invitationCode is None, expected a new code after resend"

    return True, "William Chang (pat_13) passport invitation resent successfully with updated timestamp and code"
