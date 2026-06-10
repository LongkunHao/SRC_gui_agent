import requests


def verify(server_url: str) -> tuple[bool, str]:
    """Verify Sophia Nguyen's (pat_4) message ltr_6 is marked as read."""
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, f"Failed to fetch state: HTTP {resp.status_code}"

    state = resp.json()
    letters = state.get("patientLetters", [])

    letter = None
    for l in letters:
        if l.get("id") == "ltr_6":
            letter = l
            break

    if letter is None:
        return False, "Letter ltr_6 not found in patientLetters"

    if letter.get("isRead") is not True:
        return False, f"Letter ltr_6 isRead is {letter.get('isRead')}, expected True"

    if letter.get("readAt") is None:
        return False, "Letter ltr_6 readAt is None, expected a timestamp"

    return True, "Letter ltr_6 (Sophia Nguyen, 'Appointment Request') is correctly marked as read"
