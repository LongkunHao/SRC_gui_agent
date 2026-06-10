import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()

    appt_types = state.get("appointmentTypes", [])
    for appt in appt_types:
        if appt.get("name") == "Urgent Same-Day":
            if appt.get("noteTemplate") == "tmpl_002":
                return True, "Appointment type 'Urgent Same-Day' has noteTemplate=='tmpl_002' (Problem-Focused Visit)."
            else:
                return False, f"Appointment type 'Urgent Same-Day' has noteTemplate=='{appt.get('noteTemplate')}', expected 'tmpl_002' (Problem-Focused Visit)."

    return False, "No appointment type with name 'Urgent Same-Day' found in appointmentTypes."
