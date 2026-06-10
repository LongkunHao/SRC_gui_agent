import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()

    appt_types = state.get("appointmentTypes", [])
    for appt in appt_types:
        if appt.get("name") == "COVID Vaccine":
            if appt.get("noteFormat") == "non_visit":
                return True, "Appointment type 'COVID Vaccine' has noteFormat=='non_visit'."
            else:
                return False, f"Appointment type 'COVID Vaccine' has noteFormat=='{appt.get('noteFormat')}', expected 'non_visit'."

    return False, "No appointment type with name 'COVID Vaccine' found in appointmentTypes."
