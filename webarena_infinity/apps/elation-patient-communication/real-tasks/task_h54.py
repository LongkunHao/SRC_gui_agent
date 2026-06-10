import requests


def verify(server_url: str) -> tuple[bool, str]:
    """Verify reply sent to Sophia Nguyen in conv_4 about thyroid check-up
    and rem_9 (appointment reminder) acknowledged."""
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, f"Failed to fetch state: HTTP {resp.status_code}"
    state = resp.json()

    # Check for new reply in conv_4 (Sophia Nguyen, thyroid check-up)
    seed_letter_ids = {f"ltr_{i}" for i in range(1, 48)}

    has_reply = False
    for ltr in state.get("patientLetters", []):
        if (ltr.get("conversationId") == "conv_4"
                and ltr.get("direction") == "to_patient"
                and ltr.get("id") not in seed_letter_ids
                and not ltr.get("isDraft", False)):
            has_reply = True
            break

    if not has_reply:
        return False, (
            "No new reply found in conv_4 (Sophia Nguyen's thyroid check-up request)"
        )

    # Check rem_9 acknowledged
    rem_9 = None
    for rem in state.get("reminders", []):
        if rem.get("id") == "rem_9":
            rem_9 = rem
            break

    if rem_9 is None:
        return False, "Reminder rem_9 not found in state"

    if not rem_9.get("acknowledged"):
        return False, (
            f"Reminder rem_9 (Sophia Nguyen telehealth thyroid check-up) is not acknowledged. "
            f"acknowledged={rem_9.get('acknowledged')}"
        )

    return True, (
        "Reply sent to Sophia Nguyen about scheduling thyroid check-up "
        "and rem_9 appointment reminder acknowledged"
    )
