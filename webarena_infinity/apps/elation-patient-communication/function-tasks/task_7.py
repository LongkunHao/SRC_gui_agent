import requests


def verify(server_url: str) -> tuple[bool, str]:
    """Verify a new letter was sent to David Park (pat_7) with subject 'Asthma Follow-up Scheduling'."""
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, f"Failed to fetch state: HTTP {resp.status_code}"

    state = resp.json()
    letters = state.get("patientLetters", [])

    matching = [
        l for l in letters
        if l.get("patientId") == "pat_7"
        and l.get("subject") == "Asthma Follow-up Scheduling"
        and l.get("direction") == "to_patient"
        and l.get("isDraft") is False
    ]

    if not matching:
        # Provide diagnostic info
        pat_7_letters = [l for l in letters if l.get("patientId") == "pat_7"]
        subjects = [l.get("subject") for l in pat_7_letters]
        return False, (
            f"No sent letter found for pat_7 with subject 'Asthma Follow-up Scheduling'. "
            f"David Park's letter subjects: {subjects}"
        )

    return True, "Letter sent to David Park (pat_7) with subject 'Asthma Follow-up Scheduling'"
