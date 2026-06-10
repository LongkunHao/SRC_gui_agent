import requests


def verify(server_url: str) -> tuple[bool, str]:
    """Verify Thomas Nakamura's cardiac monitoring appointment is cancelled."""
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, f"Failed to fetch state: HTTP {resp.status_code}"

    state = resp.json()
    appointments = state.get("appointments", [])

    # Find appointment for pat_17 with reason containing "Cardiac monitoring"
    for appt in appointments:
        if appt.get("patientId") != "pat_17":
            continue
        reason = appt.get("reason", "")
        if "Cardiac monitoring" not in reason:
            continue

        if appt.get("status") != "cancelled":
            return False, (
                f"Thomas Nakamura's Cardiac monitoring appointment (id={appt.get('id')}) "
                f"status is '{appt.get('status')}', expected 'cancelled'"
            )
        return True, "Thomas Nakamura's Cardiac monitoring appointment is cancelled"

    return False, "No appointment found for Thomas Nakamura (pat_17) with reason containing 'Cardiac monitoring'"
