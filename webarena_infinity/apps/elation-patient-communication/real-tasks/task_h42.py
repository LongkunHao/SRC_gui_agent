import requests


def verify(server_url: str) -> tuple[bool, str]:
    """Verify that Helen Matsumoto (pat_10) has emergency contact phone updated to (415) 555-9900
    and Passport sharing level set to 4."""
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, f"Failed to fetch state: HTTP {resp.status_code}"
    state = resp.json()

    patients = state.get("patients", [])
    if not patients:
        return False, "No patients found in state"

    pat_10 = None
    for p in patients:
        if p.get("id") == "pat_10":
            pat_10 = p
            break

    if not pat_10:
        return False, "Patient pat_10 (Helen Matsumoto) not found"

    errors = []

    # Check emergency contact phone
    ec = pat_10.get("emergencyContact", {})
    if not ec:
        errors.append("No emergency contact found for pat_10")
    else:
        phone = ec.get("phone", "")
        if phone != "(415) 555-9900":
            errors.append(f"Emergency contact phone is '{phone}', expected '(415) 555-9900'")

    # Check passport sharing level
    sharing_level = pat_10.get("passportSharingLevel")
    if sharing_level != 4:
        errors.append(f"Passport sharing level is {sharing_level}, expected 4")

    if errors:
        return False, "; ".join(errors)

    return True, "pat_10 emergency contact phone updated to (415) 555-9900 and passport sharing level set to 4"
