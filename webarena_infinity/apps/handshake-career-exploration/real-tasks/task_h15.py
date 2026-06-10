import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()

    appointments = state.get("appointments", [])
    errors = []

    for appt_id in ["appt_02", "appt_08"]:
        appt = next((a for a in appointments if a.get("id") == appt_id), None)
        if appt is None:
            errors.append(f"Appointment {appt_id} not found in state.")
        else:
            status = appt.get("status", "")
            if status != "cancelled":
                errors.append(
                    f"Appointment {appt_id} status is '{status}', expected 'cancelled'."
                )

    if errors:
        return False, " | ".join(errors)

    return True, (
        "Both requested appointments cancelled: "
        "appt_02 (Mock Interview - Technical) and appt_08 (Case Interview Prep)."
    )
