import requests


def verify(server_url: str) -> tuple[bool, str]:
    """Verify that Susan Cho's (pat_40) urticaria message (conv_28) was replied to, her virtual
    appointment (appt_14) was cancelled, and a new in-person appointment was scheduled with prov_3
    on 2026-03-12."""
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, f"Failed to fetch state: HTTP {resp.status_code}"
    state = resp.json()

    seed_letter_ids = {f"ltr_{i}" for i in range(1, 48)}
    seed_appt_ids = {f"appt_{i}" for i in range(1, 21)}
    errors = []

    # 1. Check for reply in conv_28
    reply_found = False
    for ltr in state.get("patientLetters", []):
        if (ltr.get("id") not in seed_letter_ids
                and ltr.get("conversationId") == "conv_28"
                and ltr.get("direction") == "to_patient"
                and not ltr.get("isDraft", False)):
            reply_found = True
            break

    if not reply_found:
        errors.append("No reply letter found in conv_28 (direction=to_patient)")

    # 2. Check appt_14 is cancelled
    appointments = state.get("appointments", [])
    appt_14 = None
    for appt in appointments:
        if appt.get("id") == "appt_14":
            appt_14 = appt
            break

    if not appt_14:
        errors.append("appt_14 not found in state")
    elif appt_14.get("status") != "cancelled":
        errors.append(f"appt_14 status is '{appt_14.get('status')}', expected 'cancelled'")

    # 3. Check for new in-person appointment for pat_40 with prov_3 on 2026-03-12
    new_appt_found = False
    for appt in appointments:
        if appt.get("id") in seed_appt_ids:
            continue
        if (appt.get("patientId") == "pat_40"
                and appt.get("providerId") == "prov_3"
                and appt.get("place") == "in_person"
                and "2026-03-12" in appt.get("date", "")):
            new_appt_found = True
            break

    if not new_appt_found:
        errors.append("No new in-person appointment found for pat_40 with prov_3 on 2026-03-12")

    if errors:
        return False, "; ".join(errors)

    return True, (
        "Reply sent in conv_28, appt_14 cancelled, and new in-person appointment "
        "created for pat_40 with prov_3 on 2026-03-12"
    )
