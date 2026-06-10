import requests


def verify(server_url: str) -> tuple[bool, str]:
    """Verify Marcus Johnson (pat_5) passport invitation was resent."""
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, f"Failed to fetch state: HTTP {resp.status_code}"

    state = resp.json()
    patients = state.get("patients", [])

    patient = None
    for p in patients:
        if p.get("firstName") == "Marcus" and p.get("lastName") == "Johnson":
            patient = p
            break

    if patient is None:
        return False, "Patient Marcus Johnson not found in patients"

    if patient.get("passportStatus") != "invited":
        return False, f"Marcus Johnson passportStatus is '{patient.get('passportStatus')}', expected 'invited'"

    if patient.get("invitedAt") == "2026-01-15T11:00:00Z":
        return False, "Marcus Johnson invitedAt is still the original seed value '2026-01-15T11:00:00Z', expected it to be updated after resend"

    if patient.get("invitedAt") is None:
        return False, "Marcus Johnson invitedAt is None, expected a new timestamp after resend"

    if patient.get("invitationCode") == "3847261":
        return False, "Marcus Johnson invitationCode is still the original seed value '3847261', expected a new code after resend"

    if patient.get("invitationCode") is None:
        return False, "Marcus Johnson invitationCode is None, expected a new code after resend"

    return True, "Marcus Johnson (pat_5) passport invitation resent successfully with updated timestamp and code"
