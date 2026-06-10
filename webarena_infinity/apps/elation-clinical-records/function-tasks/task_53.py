import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()

    appt_types = state.get("appointmentTypes", [])
    for appt in appt_types:
        if appt.get("name") == "Follow-Up":
            if appt.get("noteTemplate") == "tmpl_007":
                return True, "Appointment type 'Follow-Up' has noteTemplate=='tmpl_007' (Hypertension Follow-Up)."
            else:
                return False, f"Appointment type 'Follow-Up' has noteTemplate=='{appt.get('noteTemplate')}', expected 'tmpl_007' (Hypertension Follow-Up)."

    return False, "No appointment type with name 'Follow-Up' found in appointmentTypes."
