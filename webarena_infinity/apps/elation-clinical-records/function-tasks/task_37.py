import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()

    templates = state.get("visitNoteTemplates", [])
    found_virtual = False
    found_telehealth = False

    for tmpl in templates:
        name = tmpl.get("name", "")
        if name == "Virtual Visit Follow-Up":
            found_virtual = True
        if name == "Telehealth Follow-Up":
            found_telehealth = True

    if not found_virtual:
        return False, "Template 'Virtual Visit Follow-Up' not found."
    if found_telehealth:
        return False, "Template 'Telehealth Follow-Up' still exists but should have been renamed/removed."

    return True, "Template 'Virtual Visit Follow-Up' exists and 'Telehealth Follow-Up' does not."
