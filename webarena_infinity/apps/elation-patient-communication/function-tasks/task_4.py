import requests


def verify(server_url: str) -> tuple[bool, str]:
    """Verify a reply was sent in Howard Blackwell's conversation conv_24 containing 'gardening'."""
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, f"Failed to fetch state: HTTP {resp.status_code}"

    state = resp.json()
    letters = state.get("patientLetters", [])

    conv_24_to_patient = [
        l for l in letters
        if l.get("conversationId") == "conv_24" and l.get("direction") == "to_patient"
    ]

    if len(conv_24_to_patient) < 2:
        return False, (
            f"Expected at least 2 to_patient letters in conv_24, found {len(conv_24_to_patient)}. "
            f"No reply appears to have been sent."
        )

    # Find the newest to_patient letter (exclude the original ltr_33)
    new_replies = [l for l in conv_24_to_patient if l.get("id") != "ltr_33"]
    if not new_replies:
        return False, "No new reply found in conv_24 (only the original ltr_33 exists)"

    # Check any new reply contains "gardening" (case insensitive)
    for reply in new_replies:
        body = reply.get("body", "")
        if "gardening" in body.lower():
            return True, "Reply sent in conv_24 (Howard Blackwell) containing 'gardening'"

    bodies = [r.get("body", "")[:100] for r in new_replies]
    return False, f"New reply in conv_24 does not contain 'gardening' (case insensitive). Reply bodies: {bodies}"
