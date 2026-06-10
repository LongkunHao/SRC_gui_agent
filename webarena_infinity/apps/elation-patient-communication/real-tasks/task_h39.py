import requests


def verify(server_url: str) -> tuple[bool, str]:
    """Verify reply to Priya Sharma, conversation ended, Insurance Pending tag added."""
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, f"Failed to fetch state: HTTP {resp.status_code}"
    state = resp.json()

    # Priya Sharma (pat_32) asked about medical records for life insurance (conv_13)
    seed_letter_ids = {f"ltr_{i}" for i in range(1, 48)}

    # Check reply exists in conv_13
    has_reply = False
    for ltr in state.get("patientLetters", []):
        if (ltr.get("conversationId") == "conv_13"
                and ltr.get("direction") == "to_patient"
                and ltr.get("id") not in seed_letter_ids
                and not ltr.get("isDraft", False)):
            has_reply = True
            break

    if not has_reply:
        return False, "No reply found in Priya Sharma's conversation (conv_13)"

    # Check conversation is ended
    for ltr in state.get("patientLetters", []):
        if ltr.get("conversationId") == "conv_13":
            if ltr.get("conversationState") != "ended":
                return False, (
                    f"Conversation conv_13 letter {ltr.get('id')} state is "
                    f"'{ltr.get('conversationState')}', expected 'ended'"
                )

    # Check Insurance Pending tag
    pat = None
    for p in state.get("patients", []):
        if p.get("firstName") == "Priya" and p.get("lastName") == "Sharma":
            pat = p
            break

    if pat is None:
        return False, "Priya Sharma not found in patients"

    if "Insurance Pending" not in pat.get("tags", []):
        return False, (
            f"Priya Sharma is missing 'Insurance Pending' tag. "
            f"Current tags: {pat.get('tags', [])}"
        )

    return True, "Replied to Priya Sharma, ended conversation, and added Insurance Pending tag"
