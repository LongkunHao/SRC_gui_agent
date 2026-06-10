import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()

    appointment_types = state.get("appointmentTypes", [])
    target_apt = None
    for apt in appointment_types:
        if apt.get("name") == "Telehealth Visit":
            target_apt = apt
            break

    if target_apt is None:
        apt_names = [a.get("name") for a in appointment_types]
        return False, f"Could not find appointment type named 'Telehealth Visit'. Current types: {apt_names}"

    note_category = target_apt.get("noteCategory", "")
    if note_category != "cat_005":
        return False, f"Telehealth Visit noteCategory is '{note_category}', expected 'cat_005' (Follow-Up)."

    return True, "Successfully verified that Telehealth Visit appointment type now uses the Follow-Up category."
