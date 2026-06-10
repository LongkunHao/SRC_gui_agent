import requests


def verify(server_url: str) -> tuple[bool, str]:
    """Verify Anthony Petrov's EC phone updated and Passport invitation sent."""
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, f"Failed to fetch state: HTTP {resp.status_code}"
    state = resp.json()

    # Anthony Petrov (pat_9): mother as EC, tagged New Patient
    pat = None
    for p in state.get("patients", []):
        if p.get("firstName") == "Anthony" and p.get("lastName") == "Petrov":
            pat = p
            break

    if pat is None:
        return False, "Anthony Petrov not found in patients"

    # Check emergency contact phone
    ec = pat.get("emergencyContact")
    if ec is None:
        return False, "Anthony Petrov has no emergency contact"

    if ec.get("phone") != "(510) 555-8888":
        return False, (
            f"Emergency contact phone is '{ec.get('phone')}', "
            f"expected '(510) 555-8888'"
        )

    # Check Passport invitation sent
    if pat.get("passportStatus") != "invited":
        return False, (
            f"Anthony Petrov's passport status is '{pat.get('passportStatus')}', "
            f"expected 'invited'"
        )

    return True, "Anthony Petrov's EC phone updated and Passport invitation sent"
