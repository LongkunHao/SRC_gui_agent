import requests


def verify(server_url: str) -> tuple[bool, str]:
    """Verify Dennis Volkov's blood pressure management appointment is cancelled."""
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, f"Failed to fetch state: HTTP {resp.status_code}"

    state = resp.json()
    appointments = state.get("appointments", [])

    # Find appointment for pat_47 with reason containing "Blood pressure"
    for appt in appointments:
        if appt.get("patientId") != "pat_47":
            continue
        reason = appt.get("reason", "")
        if "Blood pressure" not in reason:
            continue

        if appt.get("status") != "cancelled":
            return False, (
                f"Dennis Volkov's Blood pressure management appointment (id={appt.get('id')}) "
                f"status is '{appt.get('status')}', expected 'cancelled'"
            )
        return True, "Dennis Volkov's Blood pressure management appointment is cancelled"

    return False, "No appointment found for Dennis Volkov (pat_47) with reason containing 'Blood pressure'"
