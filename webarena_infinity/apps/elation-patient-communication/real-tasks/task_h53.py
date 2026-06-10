import requests


def verify(server_url: str) -> tuple[bool, str]:
    """Verify reply to Catherine Morales in conv_27, rem_6 acknowledged,
    and pat_46 passport sharing level set to 3."""
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, f"Failed to fetch state: HTTP {resp.status_code}"
    state = resp.json()

    # Check for new reply in conv_27 (Catherine Morales, Levothyroxine question)
    seed_letter_ids = {f"ltr_{i}" for i in range(1, 48)}

    has_reply = False
    for ltr in state.get("patientLetters", []):
        if (ltr.get("conversationId") == "conv_27"
                and ltr.get("direction") == "to_patient"
                and ltr.get("id") not in seed_letter_ids
                and not ltr.get("isDraft", False)):
            has_reply = True
            break

    if not has_reply:
        return False, (
            "No new reply found in conv_27 (Catherine Morales's Levothyroxine question)"
        )

    # Check rem_6 acknowledged
    rem_6 = None
    for rem in state.get("reminders", []):
        if rem.get("id") == "rem_6":
            rem_6 = rem
            break

    if rem_6 is None:
        return False, "Reminder rem_6 not found in state"

    if not rem_6.get("acknowledged"):
        return False, (
            f"Reminder rem_6 (Catherine Morales thyroid update) is not acknowledged. "
            f"acknowledged={rem_6.get('acknowledged')}"
        )

    # Check pat_46 passport sharing level
    pat_46 = None
    for pat in state.get("patients", []):
        if pat.get("id") == "pat_46":
            pat_46 = pat
            break

    if pat_46 is None:
        return False, "Patient pat_46 (Catherine Morales) not found"

    sharing_level = pat_46.get("passportSharingLevel")
    if sharing_level != 3:
        return False, (
            f"Catherine Morales (pat_46) passport sharing level is {sharing_level}, "
            f"expected 3"
        )

    return True, (
        "Reply sent to Catherine Morales about Levothyroxine, rem_6 acknowledged, "
        "and passport sharing level set to 3"
    )
