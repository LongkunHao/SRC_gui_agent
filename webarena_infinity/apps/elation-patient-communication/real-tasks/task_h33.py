import requests


def verify(server_url: str) -> tuple[bool, str]:
    """Verify earliest registered patient's EC phone updated to (415) 555-9999."""
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, f"Failed to fetch state: HTTP {resp.status_code}"
    state = resp.json()

    # Howard Blackwell (pat_27) registered earliest on 2025-01-15
    pat = None
    for p in state.get("patients", []):
        if p.get("firstName") == "Howard" and p.get("lastName") == "Blackwell":
            pat = p
            break

    if pat is None:
        return False, "Howard Blackwell not found in patients"

    ec = pat.get("emergencyContact")
    if ec is None:
        return False, "Howard Blackwell has no emergency contact"

    if ec.get("phone") != "(415) 555-9999":
        return False, (
            f"Howard Blackwell's emergency contact phone is '{ec.get('phone')}', "
            f"expected '(415) 555-9999'"
        )

    return True, "Earliest registered patient's (Howard Blackwell) EC phone updated to (415) 555-9999"
