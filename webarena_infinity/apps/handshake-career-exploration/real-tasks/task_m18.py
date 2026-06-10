import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()

    appointments = state.get("appointments", [])
    appt_08 = next((a for a in appointments if a.get("id") == "appt_08"), None)
    if appt_08 is None:
        return False, "Appointment appt_08 not found in state."

    status = appt_08.get("status", "")

    if status == "cancelled":
        return True, "Appointment appt_08 (Case Interview Prep with James Chen) is cancelled."

    return False, (
        f"Appointment appt_08 status is '{status}', expected 'cancelled'."
    )
