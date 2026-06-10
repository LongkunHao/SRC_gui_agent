import requests


def verify(server_url: str) -> tuple[bool, str]:
    """Verify draft letter ltr_35 has been sent (isDraft=False, sentAt is set)."""
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, f"Failed to fetch state: HTTP {resp.status_code}"

    state = resp.json()
    letters = state.get("patientLetters", [])

    letter = None
    for l in letters:
        if l.get("id") == "ltr_35":
            letter = l
            break

    if letter is None:
        return False, "Letter ltr_35 not found in patientLetters (may have been deleted instead of sent)"

    if letter.get("isDraft") is not False:
        return False, f"Letter ltr_35 isDraft is {letter.get('isDraft')}, expected False"

    if letter.get("sentAt") is None:
        return False, "Letter ltr_35 sentAt is None, expected a timestamp"

    return True, "Draft letter ltr_35 has been sent (isDraft=False, sentAt is set)"
