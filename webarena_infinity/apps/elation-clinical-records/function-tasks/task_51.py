import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()

    appt_types = state.get("appointmentTypes", [])
    for appt in appt_types:
        if appt.get("name") == "Office Visit":
            if appt.get("noteFormat") == "hp_single":
                return True, "Appointment type 'Office Visit' has noteFormat=='hp_single'."
            else:
                return False, f"Appointment type 'Office Visit' has noteFormat=='{appt.get('noteFormat')}', expected 'hp_single'."

    return False, "No appointment type with name 'Office Visit' found in appointmentTypes."
