import requests


def verify(server_url: str) -> tuple[bool, str]:
    """Verify that Douglas Fitzgerald (pat_33, Geriatric + ACE intolerance) has smsOptInStatus
    set to 'opted_in', and Maria Gonzalez (pat_14, ACE intolerance) has 'High Risk' in tags."""
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, f"Failed to fetch state: HTTP {resp.status_code}"
    state = resp.json()

    patients = state.get("patients", [])
    if not patients:
        return False, "No patients found in state"

    patient_map = {p.get("id"): p for p in patients}

    errors = []

    # 1. Check pat_33 (Douglas Fitzgerald) SMS opt-in
    pat_33 = patient_map.get("pat_33")
    if not pat_33:
        errors.append("Patient pat_33 (Douglas Fitzgerald) not found")
    else:
        sms_status = pat_33.get("smsOptInStatus", "")
        if sms_status != "opted_in":
            errors.append(
                f"pat_33 smsOptInStatus is '{sms_status}', expected 'opted_in'"
            )

    # 2. Check pat_14 (Maria Gonzalez) has 'High Risk' tag
    pat_14 = patient_map.get("pat_14")
    if not pat_14:
        errors.append("Patient pat_14 (Maria Gonzalez) not found")
    else:
        tags = pat_14.get("tags", [])
        if "High Risk" not in tags:
            errors.append(f"'High Risk' not found in pat_14 tags. Current tags: {tags}")

    if errors:
        return False, "; ".join(errors)

    return True, "pat_33 SMS opted in and 'High Risk' tag added to pat_14"
