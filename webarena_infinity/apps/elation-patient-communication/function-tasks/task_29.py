import requests


SEED_APPOINTMENT_IDS = {
    "appt_1", "appt_2", "appt_3", "appt_4", "appt_5",
    "appt_6", "appt_7", "appt_8", "appt_9", "appt_10",
    "appt_11", "appt_12", "appt_13", "appt_14", "appt_15",
    "appt_16", "appt_17", "appt_18", "appt_19", "appt_20",
}


def verify(server_url: str) -> tuple[bool, str]:
    """Verify a new in-person appointment for Emily Thompson with Dr. Chen."""
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, f"Failed to fetch state: HTTP {resp.status_code}"

    state = resp.json()
    patients = state.get("patients", [])
    appointments = state.get("appointments", [])

    # Find Emily Thompson's patient ID
    emily_id = None
    for p in patients:
        if p.get("firstName") == "Emily" and p.get("lastName") == "Thompson":
            emily_id = p.get("id")
            break

    if emily_id is None:
        return False, "Patient Emily Thompson not found in patients"

    # Find new appointments (not in seed) matching criteria
    for appt in appointments:
        if appt.get("id") in SEED_APPOINTMENT_IDS:
            continue
        if appt.get("patientId") != emily_id:
            continue
        if appt.get("providerId") != "prov_1":
            continue
        if appt.get("place") != "in_person":
            continue
        if appt.get("status") != "scheduled":
            continue
        reason = (appt.get("reason") or "").lower()
        if "general check-up" not in reason:
            continue
        return True, "New in-person appointment for Emily Thompson with Dr. Chen (General check-up) found"

    return False, (
        "No new appointment found matching: Emily Thompson (pat_2), "
        "Dr. Chen (prov_1), in_person, scheduled, reason containing 'General check-up'"
    )
