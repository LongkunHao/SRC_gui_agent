import requests


def verify(server_url: str) -> tuple[bool, str]:
    """Verify reply in conv_8 (Kevin Adebayo's $247 bill conversation),
    conversation ended, and 'Insurance Pending' tag added to pat_11."""
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, f"Failed to fetch state: HTTP {resp.status_code}"
    state = resp.json()

    # Check 'Insurance Pending' tag on pat_11 (Kevin Adebayo)
    pat_11 = None
    for pat in state.get("patients", []):
        if pat.get("id") == "pat_11":
            pat_11 = pat
            break

    if pat_11 is None:
        return False, "Patient pat_11 (Kevin Adebayo) not found"

    if "Insurance Pending" not in pat_11.get("tags", []):
        return False, (
            f"Kevin Adebayo (pat_11) is missing 'Insurance Pending' tag. "
            f"Current tags: {pat_11.get('tags', [])}"
        )

    # Check for new reply in conv_8
    seed_letter_ids = {f"ltr_{i}" for i in range(1, 48)}

    conv_8_letters = [
        ltr for ltr in state.get("patientLetters", [])
        if ltr.get("conversationId") == "conv_8"
    ]

    if not conv_8_letters:
        return False, "No letters found for conversation conv_8 (Kevin Adebayo)"

    has_reply = False
    for ltr in conv_8_letters:
        if (ltr.get("id") not in seed_letter_ids
                and ltr.get("direction") == "to_patient"
                and not ltr.get("isDraft", False)):
            has_reply = True
            break

    if not has_reply:
        return False, "No new reply (to_patient) found in conversation conv_8"

    # Check that all letters in conv_8 have conversationState "ended"
    not_ended = []
    for ltr in conv_8_letters:
        if ltr.get("conversationState") != "ended":
            not_ended.append(ltr.get("id"))

    if not_ended:
        return False, (
            f"Conversation conv_8 is not fully ended. Letters without 'ended' state: "
            f"{', '.join(not_ended)}"
        )

    return True, (
        "Reply sent in conv_8 about billing, conversation ended, "
        "and 'Insurance Pending' tag added to Kevin Adebayo"
    )
