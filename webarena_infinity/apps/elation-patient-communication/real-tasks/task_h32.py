import requests


def verify(server_url: str) -> tuple[bool, str]:
    """Verify only the virtual appointment on March 5 was cancelled."""
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, f"Failed to fetch state: HTTP {resp.status_code}"
    state = resp.json()

    # appt_1: pat_1, in_person, March 5 - should remain scheduled
    # appt_14: pat_40, virtual, March 5 - should be cancelled
    appt_1 = None
    appt_14 = None
    for appt in state.get("appointments", []):
        if appt.get("id") == "appt_1":
            appt_1 = appt
        elif appt.get("id") == "appt_14":
            appt_14 = appt

    if appt_1 is None:
        return False, "Appointment appt_1 not found"
    if appt_14 is None:
        return False, "Appointment appt_14 not found"

    if appt_1.get("status") != "scheduled":
        return False, (
            f"In-person appointment (appt_1) status is '{appt_1.get('status')}', "
            f"expected 'scheduled' (should not have been cancelled)"
        )

    if appt_14.get("status") != "cancelled":
        return False, (
            f"Virtual appointment (appt_14) status is '{appt_14.get('status')}', "
            f"expected 'cancelled'"
        )

    return True, "Virtual appointment on March 5 cancelled, in-person appointment untouched"
