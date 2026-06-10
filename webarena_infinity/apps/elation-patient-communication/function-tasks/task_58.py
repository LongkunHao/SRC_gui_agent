import requests


def verify(server_url: str) -> tuple[bool, str]:
    """Verify bulk letter sent to James Rodriguez and Emily Thompson."""
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, f"Failed to fetch state: HTTP {resp.status_code}"

    state = resp.json()
    bulk_letters = state.get("bulkLetters", [])

    bulk_letter = None
    for bl in bulk_letters:
        if bl.get("subject") == "Schedule Your Annual Wellness Visit":
            bulk_letter = bl
            break

    if bulk_letter is None:
        return False, "Bulk letter with subject 'Schedule Your Annual Wellness Visit' not found"

    target_count = bulk_letter.get("targetCount")
    if target_count != 2:
        return False, f"Bulk letter targetCount is {target_count}, expected 2"

    allow_response = bulk_letter.get("allowResponse")
    if allow_response is not True:
        return False, f"Bulk letter allowResponse is {allow_response}, expected True"

    # Verify individual letters were created for pat_1 and pat_2
    patient_letters = state.get("patientLetters", [])
    subject = "Schedule Your Annual Wellness Visit"

    pat_1_letter = None
    pat_2_letter = None
    for letter in patient_letters:
        if letter.get("subject") == subject:
            if letter.get("patientId") == "pat_1":
                pat_1_letter = letter
            elif letter.get("patientId") == "pat_2":
                pat_2_letter = letter

    if pat_1_letter is None:
        return False, "No individual letter found for pat_1 (James Rodriguez) with matching subject"

    if pat_2_letter is None:
        return False, "No individual letter found for pat_2 (Emily Thompson) with matching subject"

    return True, "Bulk letter 'Schedule Your Annual Wellness Visit' correctly sent to James Rodriguez (pat_1) and Emily Thompson (pat_2)"
