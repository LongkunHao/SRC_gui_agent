import requests


def verify(server_url: str) -> tuple[bool, str]:
    """Verify reply to Andrew McIntyre, virtual appt cancelled, in-person created."""
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, f"Failed to fetch state: HTTP {resp.status_code}"
    state = resp.json()

    # Check reply in conv_16
    seed_letter_ids = {f"ltr_{i}" for i in range(1, 48)}
    has_reply = False
    for ltr in state.get("patientLetters", []):
        if (ltr.get("conversationId") == "conv_16"
                and ltr.get("direction") == "to_patient"
                and ltr.get("id") not in seed_letter_ids
                and not ltr.get("isDraft", False)):
            has_reply = True
            break

    if not has_reply:
        return False, "No reply found in Andrew McIntyre's conversation (conv_16)"

    # Check appt_6 is cancelled
    appt_6 = None
    for appt in state.get("appointments", []):
        if appt.get("id") == "appt_6":
            appt_6 = appt
            break

    if appt_6 is None:
        return False, "Appointment appt_6 not found"

    if appt_6.get("status") != "cancelled":
        return False, f"Virtual appointment appt_6 status is '{appt_6.get('status')}', expected 'cancelled'"

    # Check new in-person appointment for pat_29 on March 7
    seed_appt_ids = {f"appt_{i}" for i in range(1, 21)}
    new_in_person = None
    for appt in state.get("appointments", []):
        if (appt.get("id") not in seed_appt_ids
                and appt.get("patientId") == "pat_29"
                and appt.get("place") == "in_person"
                and appt.get("status") == "scheduled"):
            date = appt.get("date", "")
            if "2026-03-07" in date:
                new_in_person = appt
                break

    if new_in_person is None:
        return False, "No new in-person appointment found for Andrew McIntyre on March 7, 2026"

    if new_in_person.get("providerId") != "prov_2":
        return False, (
            f"New appointment provider is '{new_in_person.get('providerId')}', "
            f"expected 'prov_2' (Dr. Torres)"
        )

    return True, (
        "Replied to Andrew McIntyre, cancelled virtual appointment, "
        "and scheduled new in-person appointment for March 7"
    )
