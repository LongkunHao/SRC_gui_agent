import requests


def verify(server_url: str) -> tuple[bool, str]:
    """Verify a reply was sent in James Rodriguez's conversation conv_1 containing 'Lisinopril'."""
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, f"Failed to fetch state: HTTP {resp.status_code}"

    state = resp.json()
    letters = state.get("patientLetters", [])

    conv_1_to_patient = [
        l for l in letters
        if l.get("conversationId") == "conv_1" and l.get("direction") == "to_patient"
    ]

    if len(conv_1_to_patient) < 2:
        return False, (
            f"Expected at least 2 to_patient letters in conv_1, found {len(conv_1_to_patient)}. "
            f"No reply appears to have been sent."
        )

    # Find the newest to_patient letter (exclude the original ltr_2)
    new_replies = [l for l in conv_1_to_patient if l.get("id") != "ltr_2"]
    if not new_replies:
        return False, "No new reply found in conv_1 (only the original ltr_2 exists)"

    # Check any new reply contains "Lisinopril"
    for reply in new_replies:
        body = reply.get("body", "")
        if "Lisinopril" in body or "lisinopril" in body.lower():
            return True, "Reply sent in conv_1 (James Rodriguez) containing 'Lisinopril'"

    bodies = [r.get("body", "")[:100] for r in new_replies]
    return False, f"New reply in conv_1 does not contain 'Lisinopril'. Reply bodies: {bodies}"
