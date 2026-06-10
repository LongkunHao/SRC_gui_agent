import requests


def verify(server_url: str) -> tuple[bool, str]:
    """Verify Sophia Nguyen's thyroid check-up appointment is cancelled."""
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, f"Failed to fetch state: HTTP {resp.status_code}"

    state = resp.json()
    appointments = state.get("appointments", [])

    # Find appointment for pat_4 with reason containing "Thyroid"
    for appt in appointments:
        if appt.get("patientId") != "pat_4":
            continue
        reason = appt.get("reason", "")
        if "Thyroid" not in reason:
            continue

        if appt.get("status") != "cancelled":
            return False, (
                f"Sophia Nguyen's Thyroid check-up appointment (id={appt.get('id')}) "
                f"status is '{appt.get('status')}', expected 'cancelled'"
            )
        return True, "Sophia Nguyen's Thyroid check-up appointment is cancelled"

    return False, "No appointment found for Sophia Nguyen (pat_4) with reason containing 'Thyroid'"
