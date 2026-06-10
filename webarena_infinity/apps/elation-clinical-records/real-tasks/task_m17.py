import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()

    appointment_types = state.get("appointmentTypes", [])
    target_apt = None
    for apt in appointment_types:
        if apt.get("name") == "Office Visit":
            target_apt = apt
            break

    if target_apt is None:
        apt_names = [a.get("name") for a in appointment_types]
        return False, f"Could not find appointment type named 'Office Visit'. Current types: {apt_names}"

    note_format = target_apt.get("noteFormat", "")
    if note_format != "hp_single":
        return False, f"Office Visit noteFormat is '{note_format}', expected 'hp_single' (H&P Single Column)."

    return True, "Successfully verified that Office Visit appointment type now uses the H&P Note (Single Column) format."
