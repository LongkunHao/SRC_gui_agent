import requests


def verify(server_url: str) -> tuple[bool, str]:
    """Verify a new letter sent to Priya Sharma (pat_32) with subject 'Medical Records Information' and doNotAllowResponse == True."""
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, f"Failed to fetch state: HTTP {resp.status_code}"

    state = resp.json()
    letters = state.get("patientLetters", [])

    matching = [
        l for l in letters
        if l.get("patientId") == "pat_32"
        and l.get("subject") == "Medical Records Information"
        and l.get("direction") == "to_patient"
        and l.get("isDraft") is False
    ]

    if not matching:
        pat_32_letters = [l for l in letters if l.get("patientId") == "pat_32"]
        subjects = [l.get("subject") for l in pat_32_letters]
        return False, (
            f"No sent letter found for pat_32 with subject 'Medical Records Information'. "
            f"Priya Sharma's letter subjects: {subjects}"
        )

    letter = matching[0]
    if letter.get("doNotAllowResponse") is not True:
        return False, (
            f"Letter to Priya Sharma has doNotAllowResponse={letter.get('doNotAllowResponse')}, "
            f"expected True"
        )

    return True, "Letter sent to Priya Sharma (pat_32) with subject 'Medical Records Information' and doNotAllowResponse=True"
