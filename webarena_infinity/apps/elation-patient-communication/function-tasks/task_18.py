import requests


def verify(server_url: str) -> tuple[bool, str]:
    """Verify Brian Murphy (pat_15) has email == 'brian.murphy@gmail.com'."""
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, f"Failed to fetch state: HTTP {resp.status_code}"

    state = resp.json()
    patients = state.get("patients", [])

    patient = None
    for p in patients:
        if p.get("firstName") == "Brian" and p.get("lastName") == "Murphy":
            patient = p
            break

    if patient is None:
        return False, "Patient Brian Murphy not found in state"

    email = patient.get("email")
    if email != "brian.murphy@gmail.com":
        return False, f"Brian Murphy email is '{email}', expected 'brian.murphy@gmail.com'"

    return True, "Brian Murphy (pat_15) email is 'brian.murphy@gmail.com'"
