import requests


SEED_APPOINTMENT_IDS = {
    "appt_1", "appt_2", "appt_3", "appt_4", "appt_5",
    "appt_6", "appt_7", "appt_8", "appt_9", "appt_10",
    "appt_11", "appt_12", "appt_13", "appt_14", "appt_15",
    "appt_16", "appt_17", "appt_18", "appt_19", "appt_20",
}


def verify(server_url: str) -> tuple[bool, str]:
    """Verify a new virtual appointment for Andrew McIntyre with Dr. Torres."""
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, f"Failed to fetch state: HTTP {resp.status_code}"

    state = resp.json()
    patients = state.get("patients", [])
    appointments = state.get("appointments", [])

    # Find Andrew McIntyre's patient ID
    andrew_id = None
    for p in patients:
        if p.get("firstName") == "Andrew" and p.get("lastName") == "McIntyre":
            andrew_id = p.get("id")
            break

    if andrew_id is None:
        return False, "Patient Andrew McIntyre not found in patients"

    # Find new appointments (not in seed) matching criteria
    for appt in appointments:
        if appt.get("id") in SEED_APPOINTMENT_IDS:
            continue
        if appt.get("patientId") != andrew_id:
            continue
        if appt.get("providerId") != "prov_2":
            continue
        if appt.get("place") != "virtual":
            continue
        if appt.get("status") != "scheduled":
            continue
        reason = (appt.get("reason") or "").lower()
        if "gi follow-up" not in reason:
            continue
        return True, "New virtual appointment for Andrew McIntyre with Dr. Torres (GI follow-up) found"

    return False, (
        "No new appointment found matching: Andrew McIntyre (pat_29), "
        "Dr. Torres (prov_2), virtual, scheduled, reason containing 'GI follow-up'"
    )
