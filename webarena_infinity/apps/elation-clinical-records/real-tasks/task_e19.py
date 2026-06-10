import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()

    templates = state.get("visitNoteTemplates", [])
    found_old = False
    found_new = False
    for t in templates:
        if t.get("name") == "Telehealth Follow-Up":
            found_old = True
        if t.get("name") == "Virtual Visit Follow-Up":
            found_new = True

    if found_old:
        return False, "Template 'Telehealth Follow-Up' still exists (has not been renamed)."

    if not found_new:
        template_names = [t.get("name") for t in templates]
        return False, f"Template 'Virtual Visit Follow-Up' not found. The rename did not happen correctly. Existing templates: {template_names}"

    return True, "Successfully verified that 'Telehealth Follow-Up' has been renamed to 'Virtual Visit Follow-Up'."
