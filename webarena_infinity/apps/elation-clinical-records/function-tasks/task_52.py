import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()

    appt_types = state.get("appointmentTypes", [])
    for appt in appt_types:
        if appt.get("name") == "Telehealth Visit":
            if appt.get("noteCategory") == "cat_005":
                return True, "Appointment type 'Telehealth Visit' has noteCategory=='cat_005' (Follow-Up)."
            else:
                return False, f"Appointment type 'Telehealth Visit' has noteCategory=='{appt.get('noteCategory')}', expected 'cat_005' (Follow-Up)."

    return False, "No appointment type with name 'Telehealth Visit' found in appointmentTypes."
